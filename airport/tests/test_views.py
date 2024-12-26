import datetime
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import (
    Airplane,
    AirplaneType,
    Airport,
    Crew,
    Flight,
    Order,
    Route,
    Ticket,
)
from airport.serializers import (
    AirplaneSerializer,
    AirplaneTypeListRetrieveSerializer,
    AirportSerializer,
    FlightListSerializer,
    OrderListSerializer,
    RouteListSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
)


class ViewSetTest(TestCase):
    """Base test case class for viewset tests."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(self.user)

        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
        )

        self.airport = Airport.objects.create(
            name="Test Airport",
            closest_big_city="Test City",
        )
        self.airport2 = Airport.objects.create(
            name="Test Airport 2",
            closest_big_city="Test City 2",
        )

        self.airplane_type = AirplaneType.objects.create(name="Test Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

        self.crew = Crew.objects.create(
            first_name="Test",
            last_name="Crew",
        )

        self.route = Route.objects.create(
            source=self.airport,
            destination=self.airport2,
            distance=1000,
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + datetime.timedelta(days=1),
            arrival_time=timezone.now() + datetime.timedelta(days=1, hours=2),
        )
        self.flight.crew.add(self.crew)

        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.order,
        )

    def _create_temp_image(self) -> tempfile.NamedTemporaryFile:
        """Helper method to create temporary test image."""
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        img = Image.new("RGB", (10, 10))
        img.save(temp_file, format="JPEG")
        temp_file.seek(0)
        return temp_file


class AirportViewSetTests(ViewSetTest):
    """Test cases for Airport viewset."""

    def test_list_airports(self) -> None:
        """Test listing airports."""
        response = self.client.get(reverse("airport:airport-list"))
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_airport(self) -> None:
        """Test retrieving specific airport."""
        response = self.client.get(
            reverse("airport:airport-detail", args=[self.airport.id])
        )
        serializer = AirportSerializer(self.airport)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airport_admin(self) -> None:
        """Test creating airport by admin."""
        self.client.force_authenticate(self.admin)
        payload = {
            "name": "New Airport",
            "closest_big_city": "New City",
        }
        response = self.client.post(reverse("airport:airport-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        airport = Airport.objects.get(name=payload["name"])
        self.assertEqual(airport.closest_big_city, payload["closest_big_city"])

    def test_create_airport_forbidden(self) -> None:
        """Test creating airport by regular user is forbidden."""
        payload = {
            "name": "New Airport",
            "closest_big_city": "New City",
        }
        response = self.client.post(reverse("airport:airport-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_airport(self) -> None:
        """Test updating airport by admin."""
        self.client.force_authenticate(self.admin)
        payload = {
            "name": "Updated Airport",
            "closest_big_city": "Updated City",
        }
        response = self.client.put(
            reverse("airport:airport-detail", args=[self.airport.id]), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.airport.refresh_from_db()
        self.assertEqual(self.airport.name, payload["name"])
        self.assertEqual(self.airport.closest_big_city, payload["closest_big_city"])

    def test_delete_airport_forbidden(self) -> None:
        """Test that even admin cannot delete airport."""
        self.client.force_authenticate(self.admin)
        response = self.client.delete(
            reverse("airport:airport-detail", args=[self.airport.id])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Airport.objects.filter(id=self.airport.id).exists())

    def test_update_airport_forbidden_for_regular_user(self) -> None:
        """Test updating airport is forbidden for regular user."""
        payload = {
            "name": "Updated Airport",
            "closest_big_city": "Updated City",
        }
        response = self.client.put(
            reverse("airport:airport-detail", args=[self.airport.id]), payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_airport_forbidden_for_regular_user(self) -> None:
        """Test deleting airport is forbidden for regular user."""
        response = self.client.delete(
            reverse("airport:airport-detail", args=[self.airport.id])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AirplaneTypeViewSetTests(ViewSetTest):
    """Test cases for AirplaneType viewset."""

    def test_list_airplane_types(self) -> None:
        """Test listing airplane types."""
        response = self.client.get(reverse("airport:airplane-type-list"))
        airplane_types = AirplaneType.objects.all()
        serializer = AirplaneTypeListRetrieveSerializer(airplane_types, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data[0]
        serializer_data = serializer.data[0]

        self.assertEqual(response_data["id"], serializer_data["id"])
        self.assertEqual(response_data["name"], serializer_data["name"])
        self.assertEqual(response_data["airplanes_count"], 1)

    def test_create_airplane_type(self) -> None:
        """Test creating airplane type by admin."""
        self.client.force_authenticate(self.admin)
        payload = {"name": "New Type"}
        response = self.client.post(reverse("airport:airplane-type-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AirplaneType.objects.filter(name=payload["name"]).exists())

    def test_update_airplane_type(self) -> None:
        """Test updating airplane type."""
        self.client.force_authenticate(self.admin)
        payload = {"name": "Updated Type"}
        response = self.client.put(
            reverse("airport:airplane-type-detail", args=[self.airplane_type.id]),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.airplane_type.refresh_from_db()
        self.assertEqual(self.airplane_type.name, payload["name"])


class AirplaneViewSetTests(ViewSetTest):
    """Test cases for Airplane viewset."""

    def test_list_airplanes(self) -> None:
        """Test listing airplanes."""
        response = self.client.get(reverse("airport:airplane-list"))
        airplanes = Airplane.objects.all()
        serializer = AirplaneSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data["results"][0]
        serializer_data = serializer.data[0]

        self.assertEqual(response_data["name"], serializer_data["name"])
        self.assertEqual(response_data["rows"], serializer_data["rows"])
        self.assertEqual(response_data["seats_in_row"], serializer_data["seats_in_row"])
        self.assertEqual(response_data["image"], serializer_data["image"])

    def test_filter_by_airplane_type(self) -> None:
        """Test filtering airplanes by type."""
        response = self.client.get(
            reverse("airport:airplane-list"),
            {"airplane_type": self.airplane_type.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["airplane_type_name"],
            str(self.airplane_type.name),
        )

    def test_create_airplane(self) -> None:
        """Test creating airplane by admin."""
        self.client.force_authenticate(self.admin)
        payload = {
            "name": "New Airplane",
            "rows": 20,
            "seats_in_row": 4,
            "airplane_type": self.airplane_type.id,
        }
        response = self.client.post(reverse("airport:airplane-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Airplane.objects.filter(name=payload["name"]).exists())

    def test_upload_airplane_image(self) -> None:
        """Test uploading airplane image."""
        self.client.force_authenticate(self.admin)

        with self._create_temp_image() as image_file:
            response = self.client.post(
                reverse("airport:airplane-upload-image", args=[self.airplane.id]),
                {"image": image_file},
                format="multipart",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.airplane.refresh_from_db()
        self.assertTrue(self.airplane.image)

    def test_upload_image_forbidden_for_regular_user(self) -> None:
        """Test uploading airplane image is forbidden for regular user."""
        with self._create_temp_image() as image_file:
            response = self.client.post(
                reverse("airport:airplane-upload-image", args=[self.airplane.id]),
                {"image": image_file},
                format="multipart",
            )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CrewViewSetTests(ViewSetTest):
    """Test cases for Crew viewset."""

    def test_list_crew(self) -> None:
        """Test listing crew members."""
        response = self.client.get(reverse("airport:crew-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [dict(item) for item in response.data],
            [
                {
                    "id": str(crew.id),
                    "full_name": crew.full_name,
                    "flights_count": crew.flights.count(),
                }
                for crew in Crew.objects.all()
            ],
        )

    def test_create_crew(self) -> None:
        """Test creating crew member."""
        self.client.force_authenticate(self.admin)
        payload = {"first_name": "New", "last_name": "Crew"}
        response = self.client.post(reverse("airport:crew-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Crew.objects.filter(
                first_name=payload["first_name"], last_name=payload["last_name"]
            ).exists()
        )


class RouteViewSetTests(ViewSetTest):
    """Test cases for Route viewset."""

    def test_list_routes(self) -> None:
        """Test listing routes."""
        response = self.client.get(reverse("airport:route-list"))
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_source_destination(self) -> None:
        """Test filtering routes by source and destination."""
        response = self.client.get(
            reverse("airport:route-list"),
            {
                "source": self.airport.id,
                "destination": self.airport2.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["source_name"],
            self.airport.name,
        )
        self.assertEqual(
            response.data[0]["destination_name"],
            self.airport2.name,
        )

    def test_create_route(self) -> None:
        """Test creating route."""
        self.client.force_authenticate(self.admin)

        new_airport = Airport.objects.create(
            name="Test Airport 3",
            closest_big_city="Test City 3",
        )

        payload = {
            "source": self.airport.id,
            "destination": new_airport.id,
            "distance": 2000,
        }
        response = self.client.post(
            reverse("airport:route-list"),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Route.objects.filter(distance=payload["distance"]).exists())


class FlightViewSetTests(ViewSetTest):
    """Test cases for Flight viewset."""

    def test_list_flights(self) -> None:
        """Test listing flights."""
        response = self.client.get(reverse("airport:flight-list"))
        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_by_date(self) -> None:
        """Test filtering flights by date."""
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        response = self.client.get(
            reverse("airport:flight-list"),
            {"date": tomorrow.date().isoformat()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_flight(self) -> None:
        """Test creating flight."""
        self.client.force_authenticate(self.admin)
        departure = timezone.now() + datetime.timedelta(days=2)
        arrival = departure + datetime.timedelta(hours=2)

        payload = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": departure.isoformat(),
            "arrival_time": arrival.isoformat(),
            "crew": [self.crew.id],
        }
        response = self.client.post(
            reverse("airport:flight-list"), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        flight = Flight.objects.get(id=response.data["id"])
        self.assertEqual(flight.crew.count(), 1)


class OrderViewSetTests(ViewSetTest):
    """Test cases for Order viewset."""

    def test_list_orders(self) -> None:
        """Test listing orders."""
        response = self.client.get(reverse("airport:order-list"))
        orders = Order.objects.filter(user=self.user)
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_order(self) -> None:
        """Test creating order."""
        payload = {
            "tickets": [
                {
                    "row": 2,
                    "seat": 2,
                    "flight": self.flight.id,
                }
            ]
        }
        response = self.client.post(
            reverse("airport:order-list"), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.tickets.count(), 1)
        self.assertEqual(order.user, self.user)

    def test_create_order_invalid_seat(self) -> None:
        """Test creating order with invalid seat."""
        payload = {
            "tickets": [
                {
                    "row": 11,
                    "seat": 1,
                    "flight": self.flight.id,
                }
            ]
        }
        response = self.client.post(
            reverse("airport:order-list"), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TicketViewSetTests(ViewSetTest):
    """Test cases for Ticket viewset."""

    def test_list_tickets(self) -> None:
        """Test listing tickets."""
        response = self.client.get(reverse("airport:ticket-list"))
        tickets = Ticket.objects.filter(order__user=self.user)
        serializer = TicketListSerializer(tickets, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_ticket(self) -> None:
        """Test retrieving specific ticket."""
        response = self.client.get(
            reverse("airport:ticket-detail", args=[self.ticket.id])
        )
        serializer = TicketDetailSerializer(self.ticket)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_other_user_ticket_forbidden(self) -> None:
        """Test retrieving ticket of another user is forbidden."""
        other_user = get_user_model().objects.create_user(
            email="other@test.com",
            password="testpass123",
            first_name="Other",
            last_name="User",
        )
        other_order = Order.objects.create(user=other_user)
        other_ticket = Ticket.objects.create(
            row=2,
            seat=2,
            flight=self.flight,
            order=other_order,
        )

        response = self.client.get(
            reverse("airport:ticket-detail", args=[other_ticket.id])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
