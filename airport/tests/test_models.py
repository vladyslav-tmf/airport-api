import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
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


User = get_user_model()


class AirportTests(TestCase):
    """Test the Airport model."""

    def setUp(self) -> None:
        self.airport = Airport.objects.create(
            name="Test Airport",
            closest_big_city="Test City",
        )

    def test_airport_str(self) -> None:
        """Test the string representation of Airport."""
        self.assertEqual(
            str(self.airport),
            f"{self.airport.name} ({self.airport.closest_big_city})",
        )

    def test_airport_ordering(self) -> None:
        """Test that airports are ordered by name."""
        Airport.objects.create(name="A Airport", closest_big_city="A City")
        Airport.objects.create(name="C Airport", closest_big_city="C City")

        airports = Airport.objects.all()
        self.assertEqual(airports[0].name, "A Airport")
        self.assertEqual(airports[1].name, "C Airport")
        self.assertEqual(airports[2].name, "Test Airport")

    def test_unique_name_constraint(self) -> None:
        """Test that airport name must be unique."""
        with self.assertRaises(IntegrityError):
            Airport.objects.create(
                name="Test Airport",
                closest_big_city="Another City",
            )


class AirplaneTypeTests(TestCase):
    """Test the AirplaneType model."""

    def setUp(self) -> None:
        self.airplane_type = AirplaneType.objects.create(name="Test Type")

    def test_airplane_type_str(self) -> None:
        """Test the string representation of AirplaneType."""
        self.assertEqual(str(self.airplane_type), self.airplane_type.name)

    def test_unique_name_constraint(self) -> None:
        """Test that airplane type name must be unique."""
        with self.assertRaises(IntegrityError):
            AirplaneType.objects.create(name="Test Type")


class AirplaneTests(TestCase):
    """Test the Airplane model."""

    def setUp(self) -> None:
        self.airplane_type = AirplaneType.objects.create(name="Test Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

    def test_airplane_str(self) -> None:
        """Test the string representation of Airplane."""
        self.assertEqual(
            str(self.airplane), f"{self.airplane_type.name} {self.airplane.name}"
        )

    def test_total_seats(self) -> None:
        """Test calculating total seats."""
        self.assertEqual(self.airplane.total_seats, 60)

    def test_unique_name_type_constraint(self) -> None:
        """Test that airplane name must be unique within type."""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Airplane.objects.create(
                    name="Test Airplane",
                    rows=8,
                    seats_in_row=4,
                    airplane_type=self.airplane_type,
                )

        with transaction.atomic():
            other_type = AirplaneType.objects.create(name="Other Type")
            Airplane.objects.create(
                name="Test Airplane",
                rows=8,
                seats_in_row=4,
                airplane_type=other_type,
            )


class CrewTests(TestCase):
    """Test the Crew model."""

    def setUp(self) -> None:
        self.crew = Crew.objects.create(
            first_name="Test",
            last_name="Crew",
        )

    def test_crew_str(self) -> None:
        """Test the string representation of Crew."""
        self.assertEqual(
            str(self.crew),
            f"{self.crew.first_name} {self.crew.last_name}",
        )

    def test_crew_full_name(self) -> None:
        """Test the full_name property."""
        self.assertEqual(
            self.crew.full_name,
            f"{self.crew.first_name} {self.crew.last_name}",
        )

    def test_crew_ordering(self) -> None:
        """Test that crew members are ordered by last name, first name."""
        Crew.objects.create(first_name="A", last_name="Z")
        Crew.objects.create(first_name="B", last_name="A")

        crew = Crew.objects.all()
        self.assertEqual(crew[0].last_name, "A")
        self.assertEqual(crew[1].last_name, "Crew")
        self.assertEqual(crew[2].last_name, "Z")


class RouteTests(TestCase):
    """Test the Route model."""

    def setUp(self) -> None:
        self.airport1 = Airport.objects.create(
            name="Airport 1",
            closest_big_city="City 1",
        )
        self.airport2 = Airport.objects.create(
            name="Airport 2",
            closest_big_city="City 2",
        )
        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=1000,
        )

    def test_route_str(self) -> None:
        """Test the string representation of Route."""
        expected = f"{self.route.source.name} → {self.route.destination.name} (1000 km)"
        self.assertEqual(str(self.route), expected)

    def test_same_airports_validation(self) -> None:
        """Test validation prevents same source and destination."""
        with self.assertRaises(ValidationError):
            route = Route(
                source=self.airport1,
                destination=self.airport1,
                distance=100,
            )
            route.full_clean()

    def test_distance_validation(self) -> None:
        """Test validation of distance."""
        with self.assertRaises(ValidationError):
            route = Route(
                source=self.airport1,
                destination=self.airport2,
                distance=25000,
            )
            route.full_clean()

    def test_unique_route_constraint(self) -> None:
        """Test that route must be unique."""
        with self.assertRaises(IntegrityError):
            Route.objects.create(
                source=self.airport1,
                destination=self.airport2,
                distance=1500,
            )


class FlightTests(TestCase):
    """Test the Flight model."""

    def setUp(self) -> None:
        self.airport1 = Airport.objects.create(
            name="Airport 1",
            closest_big_city="City 1",
        )
        self.airport2 = Airport.objects.create(
            name="Airport 2",
            closest_big_city="City 2",
        )
        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=1000,
        )
        self.airplane_type = AirplaneType.objects.create(name="Test Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.departure_time = timezone.now() + datetime.timedelta(days=1)
        self.arrival_time = self.departure_time + datetime.timedelta(hours=2)
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=self.departure_time,
            arrival_time=self.arrival_time,
        )

    def test_flight_str(self) -> None:
        """Test the string representation of Flight."""
        expected = (
            f"{self.flight.route.source.name} "
            f"({self.departure_time.strftime('%Y.%m.%d %H:%M')}) → "
            f"{self.flight.route.destination.name} "
            f"({self.arrival_time.strftime('%Y.%m.%d %H:%M')})"
        )
        self.assertEqual(str(self.flight), expected)

    def test_arrival_before_departure_validation(self) -> None:
        """Test validation prevents arrival before departure."""
        with self.assertRaises(ValidationError):
            flight = Flight(
                route=self.route,
                airplane=self.airplane,
                departure_time=self.departure_time,
                arrival_time=self.departure_time - datetime.timedelta(hours=1),
            )
            flight.full_clean()

    def test_available_seats(self) -> None:
        """Test calculating available seats."""
        self.assertEqual(self.flight.available_seats, 60)

        order = Order.objects.create(
            user=User.objects.create_user(
                email="test@test.com",
                password="testpass123",
                first_name="Test",
                last_name="User",
            )
        )
        Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=order,
        )

        self.assertEqual(self.flight.available_seats, 59)


class OrderTests(TestCase):
    """Test the Order model."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.order = Order.objects.create(user=self.user)

    def test_order_str(self) -> None:
        """Test the string representation of Order."""
        expected = f'Order "{self.order.id}" by {self.user.get_full_name()}'
        self.assertEqual(str(self.order), expected)

    def test_order_ordering(self) -> None:
        """Test that orders are ordered by created_at in descending order."""
        order2 = Order.objects.create(user=self.user)
        orders = Order.objects.all()
        self.assertEqual(orders[0], order2)
        self.assertEqual(orders[1], self.order)


class TicketTests(TestCase):
    """Test the Ticket model."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.airport1 = Airport.objects.create(
            name="Airport 1",
            closest_big_city="City 1",
        )
        self.airport2 = Airport.objects.create(
            name="Airport 2",
            closest_big_city="City 2",
        )
        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=1000,
        )
        self.airplane_type = AirplaneType.objects.create(name="Test Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + datetime.timedelta(days=1),
            arrival_time=timezone.now() + datetime.timedelta(days=1, hours=2),
        )
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.order,
        )

    def test_ticket_str(self) -> None:
        """Test the string representation of Ticket."""
        expected = (
            f"{self.flight.route.source.closest_big_city} → "
            f"{self.flight.route.destination.closest_big_city} "
            f"(Departure at {self.flight.departure_time.strftime('%Y.%m.%d %H:%M')}): "
            f"seat {self.ticket.row}-{self.ticket.seat}"
        )
        self.assertEqual(str(self.ticket), expected)

    def test_seat_number(self) -> None:
        """Test the seat_number property."""
        self.assertEqual(self.ticket.seat_number, "1-1")

    def test_validate_ticket_invalid_row(self) -> None:
        """Test validation with invalid row number."""
        with self.assertRaises(ValidationError):
            ticket = Ticket(
                row=11,
                seat=1,
                flight=self.flight,
                order=self.order,
            )
            ticket.full_clean()

    def test_validate_ticket_invalid_seat(self) -> None:
        """Test validation with invalid seat number."""
        with self.assertRaises(ValidationError):
            ticket = Ticket(
                row=1,
                seat=7,
                flight=self.flight,
                order=self.order,
            )
            ticket.full_clean()

    def test_unique_seat_constraint(self) -> None:
        """Test that seat must be unique within a flight."""
        with self.assertRaises(IntegrityError):
            Ticket.objects.create(
                row=1,
                seat=1,
                flight=self.flight,
                order=self.order,
            )

    def test_past_flight_validation(self) -> None:
        """Test validation prevents tickets for past flights."""
        past_flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() - datetime.timedelta(days=1),
            arrival_time=timezone.now() - datetime.timedelta(hours=22),
        )
        with self.assertRaises(ValidationError):
            ticket = Ticket(
                row=1,
                seat=1,
                flight=past_flight,
                order=self.order,
            )
            ticket.full_clean()
