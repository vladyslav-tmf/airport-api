import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

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
    AirplaneDetailSerializer,
    AirplaneImageSerializer,
    AirplaneListSerializer,
    AirplaneSerializer,
    AirplaneTypeListRetrieveSerializer,
    AirplaneTypeSerializer,
    AirportSerializer,
    CrewListSerializer,
    CrewSerializer,
    FlightDetailSerializer,
    FlightListSerializer,
    FlightSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderSerializer,
    RouteDetailSerializer,
    RouteListSerializer,
    RouteSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketSerializer,
)


class SerializerTestCase(TestCase):
    """Base test case class for serializer tests."""
    def setUp(self) -> None:
        """Set up test data for all serializer tests."""
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
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


class AirportSerializerTests(SerializerTestCase):
    """Test cases for Airport serializers."""
    def test_airport_serializer(self) -> None:
        """Test AirportSerializer."""
        serializer = AirportSerializer(self.airport)
        expected_data = {
            "id": str(self.airport.id),
            "name": "Test Airport",
            "closest_big_city": "Test City",
        }
        self.assertEqual(serializer.data, expected_data)


class AirplaneTypeSerializerTests(SerializerTestCase):
    """Test cases for AirplaneType serializers."""
    def test_airplane_type_serializer(self) -> None:
        """Test AirplaneTypeSerializer."""
        serializer = AirplaneTypeSerializer(self.airplane_type)
        expected_data = {
            "id": str(self.airplane_type.id),
            "name": "Test Type",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_airplane_type_list_retrieve_serializer(self) -> None:
        """Test AirplaneTypeListRetrieveSerializer."""
        serializer = AirplaneTypeListRetrieveSerializer(self.airplane_type)
        expected_data = {
            "id": str(self.airplane_type.id),
            "name": "Test Type",
        }
        self.assertEqual(serializer.data, expected_data)


class AirplaneSerializerTests(SerializerTestCase):
    """Test cases for Airplane serializers."""
    def test_airplane_serializer(self) -> None:
        """Test AirplaneSerializer."""
        serializer = AirplaneSerializer(self.airplane)
        expected_data = {
            "id": str(self.airplane.id),
            "name": "Test Airplane",
            "rows": 10,
            "seats_in_row": 6,
            "total_seats": 60,
            "airplane_type": self.airplane_type.id,
            "image": None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_airplane_list_serializer(self) -> None:
        """Test AirplaneListSerializer."""
        serializer = AirplaneListSerializer(self.airplane)
        expected_data = {
            "id": str(self.airplane.id),
            "name": "Test Airplane",
            "rows": 10,
            "seats_in_row": 6,
            "total_seats": 60,
            "airplane_type_name": "Test Type",
            "image": None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_airplane_detail_serializer(self) -> None:
        """Test AirplaneDetailSerializer."""
        serializer = AirplaneDetailSerializer(self.airplane)
        expected_data = {
            "id": str(self.airplane.id),
            "name": "Test Airplane",
            "rows": 10,
            "seats_in_row": 6,
            "total_seats": 60,
            "airplane_type": {
                "id": str(self.airplane_type.id),
                "name": "Test Type",
            },
            "image": None,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_airplane_image_serializer(self) -> None:
        """Test AirplaneImageSerializer."""
        serializer = AirplaneImageSerializer(self.airplane)
        expected_data = {
            "id": str(self.airplane.id),
            "image": None,
        }
        self.assertEqual(serializer.data, expected_data)


class CrewSerializerTests(SerializerTestCase):
    """Test cases for Crew serializers."""
    def test_crew_serializer(self) -> None:
        """Test CrewSerializer."""
        serializer = CrewSerializer(self.crew)
        expected_data = {
            "id": str(self.crew.id),
            "first_name": "Test",
            "last_name": "Crew",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_crew_list_serializer(self) -> None:
        """Test CrewListSerializer."""
        serializer = CrewListSerializer(self.crew)
        expected_data = {
            "id": str(self.crew.id),
            "full_name": "Test Crew",
        }
        self.assertEqual(serializer.data, expected_data)


class RouteSerializerTests(SerializerTestCase):
    """Test cases for Route serializers."""
    def test_route_serializer(self) -> None:
        """Test RouteSerializer."""
        serializer = RouteSerializer(self.route)
        expected_data = {
            "id": str(self.route.id),
            "source": self.airport.id,
            "destination": self.airport2.id,
            "distance": 1000,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_route_list_serializer(self) -> None:
        """Test RouteListSerializer."""
        serializer = RouteListSerializer(self.route)
        expected_data = {
            "id": str(self.route.id),
            "source_name": "Test Airport",
            "destination_name": "Test Airport 2",
            "distance": 1000,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_route_detail_serializer(self) -> None:
        """Test RouteDetailSerializer."""
        serializer = RouteDetailSerializer(self.route)
        expected_data = {
            "id": str(self.route.id),
            "source": {
                "id": str(self.airport.id),
                "name": "Test Airport",
                "closest_big_city": "Test City",
            },
            "destination": {
                "id": str(self.airport2.id),
                "name": "Test Airport 2",
                "closest_big_city": "Test City 2",
            },
            "distance": 1000,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_route_validation(self) -> None:
        """Test route validation."""
        data = {
            "source": self.airport.id,
            "destination": self.airport.id,
            "distance": 1000,
        }
        serializer = RouteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("destination", serializer.errors)

        airport3 = Airport.objects.create(
            name="Test Airport 3",
            closest_big_city="Test City 3",
        )
        data = {
            "source": self.airport.id,
            "destination": airport3.id,
            "distance": 25000,
        }
        serializer = RouteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("distance", serializer.errors)


class FlightSerializerTests(SerializerTestCase):
    """Test cases for Flight serializers."""
    def test_flight_serializer(self) -> None:
        """Test FlightSerializer."""
        serializer = FlightSerializer(self.flight)
        expected_data = {
            "id": str(self.flight.id),
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": (
                timezone.localtime(self.flight.departure_time).isoformat()
            ),
            "arrival_time": timezone.localtime(self.flight.arrival_time).isoformat(),
            "available_seats": 59,
            "crew": [self.crew.id],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_flight_list_serializer(self) -> None:
        """Test FlightListSerializer."""
        serializer = FlightListSerializer(self.flight)
        expected_data = {
            "id": str(self.flight.id),
            "source_airport": "Test Airport",
            "destination_airport": "Test Airport 2",
            "airplane_name": "Test Airplane",
            "departure_time": (
                timezone.localtime(self.flight.departure_time).isoformat()
            ),
            "arrival_time": timezone.localtime(self.flight.arrival_time).isoformat(),
            "available_seats": 59,
            "crew_names": ["Test Crew"],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_flight_detail_serializer(self) -> None:
        """Test FlightDetailSerializer."""
        serializer = FlightDetailSerializer(self.flight)
        expected_data = {
            "id": str(self.flight.id),
            "route": {
                "id": str(self.route.id),
                "source": {
                    "id": str(self.airport.id),
                    "name": "Test Airport",
                    "closest_big_city": "Test City",
                },
                "destination": {
                    "id": str(self.airport2.id),
                    "name": "Test Airport 2",
                    "closest_big_city": "Test City 2",
                },
                "distance": 1000,
            },
            "airplane": {
                "id": str(self.airplane.id),
                "name": "Test Airplane",
                "rows": 10,
                "seats_in_row": 6,
                "total_seats": 60,
                "airplane_type_name": "Test Type",
                "image": None,
            },
            "departure_time": (
                timezone.localtime(self.flight.departure_time).isoformat()
            ),
            "arrival_time": timezone.localtime(self.flight.arrival_time).isoformat(),
            "available_seats": 59,
            "crew": [{
                "id": str(self.crew.id),
                "full_name": "Test Crew",
            }],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_flight_validation(self) -> None:
        """Test flight validation."""
        data = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": timezone.now(),
            "arrival_time": timezone.now() - datetime.timedelta(hours=1),
            "crew": [self.crew.id],
        }
        serializer = FlightSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("arrival_time", serializer.errors)


class OrderSerializerTests(SerializerTestCase):
    """Test cases for Order serializers."""
    def test_order_serializer(self) -> None:
        """Test OrderSerializer."""
        serializer = OrderSerializer(self.order)
        expected_data = {
            "id": str(self.order.id),
            "created_at": timezone.localtime(self.order.created_at).isoformat(),
            "tickets": [{
                "id": str(self.ticket.id),
                "row": 1,
                "seat": 1,
                "flight": self.flight.id,
            }],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_order_list_serializer(self) -> None:
        """Test OrderListSerializer."""
        serializer = OrderListSerializer(self.order)
        expected_data = {
            "id": str(self.order.id),
            "user_full_name": "Test User",
            "tickets_count": 1,
            "created_at": timezone.localtime(self.order.created_at).isoformat(),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_order_detail_serializer(self) -> None:
        """Test OrderDetailSerializer."""
        serializer = OrderDetailSerializer(self.order)
        self.assertEqual(serializer.data["id"], str(self.order.id))
        self.assertEqual(serializer.data["user_full_name"], "Test User")
        self.assertEqual(len(serializer.data["tickets"]), 1)


class TicketSerializerTests(SerializerTestCase):
    """Test cases for Ticket serializers."""
    def test_ticket_serializer(self) -> None:
        """Test TicketSerializer."""
        serializer = TicketSerializer(self.ticket)
        expected_data = {
            "id": str(self.ticket.id),
            "row": 1,
            "seat": 1,
            "flight": self.flight.id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_ticket_list_serializer(self) -> None:
        """Test TicketListSerializer."""
        serializer = TicketListSerializer(self.ticket)
        expected_data = {
            "id": str(self.ticket.id),
            "row": 1,
            "seat": 1,
            "seat_number": "1-1",
            "source_city": "Test City",
            "destination_city": "Test City 2",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_ticket_detail_serializer(self) -> None:
        """Test TicketDetailSerializer."""
        serializer = TicketDetailSerializer(self.ticket)
        expected_data = {
            "id": str(self.ticket.id),
            "row": 1,
            "seat": 1,
            "flight": {
                "id": str(self.flight.id),
                "route": {
                    "id": str(self.route.id),
                    "source": {
                        "id": str(self.airport.id),
                        "name": "Test Airport",
                        "closest_big_city": "Test City",
                    },
                    "destination": {
                        "id": str(self.airport2.id),
                        "name": "Test Airport 2",
                        "closest_big_city": "Test City 2",
                    },
                    "distance": 1000,
                },
                "airplane": {
                    "id": str(self.airplane.id),
                    "name": "Test Airplane",
                    "rows": 10,
                    "seats_in_row": 6,
                    "total_seats": 60,
                    "airplane_type_name": "Test Type",
                    "image": None,
                },
                "departure_time": (
                    timezone.localtime(self.flight.departure_time).isoformat()
                ),
                "arrival_time": (
                    timezone.localtime(self.flight.arrival_time).isoformat()
                ),
                "available_seats": 59,
                "crew": [{
                    "id": str(self.crew.id),
                    "full_name": "Test Crew",
                }],
            },
            "order": self.ticket.order.id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_ticket_validation(self) -> None:
        """Test ticket validation."""
        data = {
            "row": 11,
            "seat": 1,
            "flight": self.flight.id,
        }
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("row", serializer.errors)

        data = {
            "row": 1,
            "seat": 7,
            "flight": self.flight.id,
        }
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("seat", serializer.errors)
