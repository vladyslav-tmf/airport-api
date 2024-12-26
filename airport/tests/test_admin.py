import datetime

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from airport.admin import (
    AirplaneAdmin,
    AirplaneTypeAdmin,
    AirportAdmin,
    CrewAdmin,
    FlightAdmin,
    OrderAdmin,
    RouteAdmin,
    TicketAdmin,
)
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


class AdminSiteTestCase(TestCase):
    """Base test case class for admin site tests."""
    def setUp(self) -> None:
        """Set up test data."""
        self.site = AdminSite()
        self.client = Client()

        self.admin_user = User.objects.create_superuser(
            email="admin@test.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
        )
        self.client.force_login(self.admin_user)

        self.airport = Airport.objects.create(
            name="Test Airport",
            closest_big_city="Test City",
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
            destination=Airport.objects.create(
                name="Test Airport 2",
                closest_big_city="Test City 2",
            ),
            distance=1000,
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + datetime.timedelta(days=1),
            arrival_time=timezone.now() + datetime.timedelta(days=1, hours=2),
        )
        self.flight.crew.add(self.crew)

        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.order,
        )


class AirportAdminTests(AdminSiteTestCase):
    """Test cases for Airport admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = AirportAdmin(Airport, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(
            self.admin.list_display,
            ("name", "closest_big_city"),
        )

    def test_search_fields(self) -> None:
        """Test search_fields settings."""
        self.assertEqual(
            self.admin.search_fields,
            ("name", "closest_big_city"),
        )

    def test_list_filter(self) -> None:
        """Test list_filter settings."""
        self.assertEqual(
            self.admin.list_filter,
            ("closest_big_city",),
        )

    def test_admin_page_loads(self) -> None:
        """Test that admin page loads successfully."""
        url = reverse("admin:airport_airport_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_search(self) -> None:
        """Test search functionality in admin."""
        url = reverse("admin:airport_airport_changelist")
        response = self.client.get(url, {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Airport")

    def test_admin_add_edit(self) -> None:
        """Test adding and editing objects through admin."""
        add_url = reverse("admin:airport_airport_add")
        response = self.client.post(
            add_url, {
                "name": "New Airport",
                "closest_big_city": "New City"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Airport.objects.filter(name="New Airport").exists())

        airport = Airport.objects.get(name="New Airport")
        edit_url = reverse("admin:airport_airport_change", args=[airport.id])
        response = self.client.post(
            edit_url, {
                "name": "Updated Airport",
                "closest_big_city": "Updated City"
            }
        )
        self.assertEqual(response.status_code, 302)
        airport.refresh_from_db()
        self.assertEqual(airport.name, "Updated Airport")


class AirplaneTypeAdminTests(AdminSiteTestCase):
    """Test cases for AirplaneType admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = AirplaneTypeAdmin(AirplaneType, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(self.admin.list_display, ("name",))

    def test_search_fields(self) -> None:
        """Test search_fields settings."""
        self.assertEqual(self.admin.search_fields, ("name",))


class AirplaneAdminTests(AdminSiteTestCase):
    """Test cases for Airplane admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = AirplaneAdmin(Airplane, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(
            self.admin.list_display,
            ("name", "airplane_type", "rows", "seats_in_row", "total_seats"),
        )

    def test_list_filter(self) -> None:
        """Test list_filter settings."""
        self.assertEqual(self.admin.list_filter, ("airplane_type",))

    def test_search_fields(self) -> None:
        """Test search_fields settings."""
        self.assertEqual(
            self.admin.search_fields,
            ("name", "airplane_type__name"),
        )


class CrewAdminTests(AdminSiteTestCase):
    """Test cases for Crew admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = CrewAdmin(Crew, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(
            self.admin.list_display,
            ("first_name", "last_name"),
        )

    def test_search_fields(self) -> None:
        """Test search_fields settings."""
        self.assertEqual(
            self.admin.search_fields,
            ("first_name", "last_name"),
        )


class RouteAdminTests(AdminSiteTestCase):
    """Test cases for Route admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = RouteAdmin(Route, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(
            self.admin.list_display,
            ("source", "destination", "distance"),
        )

    def test_list_filter(self) -> None:
        """Test list_filter settings."""
        self.assertEqual(
            self.admin.list_filter,
            ("source", "destination"),
        )

    def test_search_fields(self) -> None:
        """Test search_fields settings."""
        self.assertEqual(
            self.admin.search_fields,
            ("source__name", "destination__name"),
        )


class FlightAdminTests(AdminSiteTestCase):
    """Test cases for Flight admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = FlightAdmin(Flight, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(
            self.admin.list_display,
            ("route", "airplane", "departure_time", "arrival_time", "available_seats"),
        )

    def test_list_filter(self) -> None:
        """Test list_filter settings."""
        self.assertEqual(
            self.admin.list_filter,
            ("route__source", "route__destination", "departure_time", "crew"),
        )

    def test_search_fields(self) -> None:
        """Test search_fields settings."""
        self.assertEqual(
            self.admin.search_fields,
            (
                "route__source__name",
                "route__source__closest_big_city",
                "route__destination__name",
                "route__destination__closest_big_city",
                "airplane__name",
            ),
        )

    def test_date_hierarchy(self) -> None:
        """Test date_hierarchy setting."""
        self.assertEqual(self.admin.date_hierarchy, "departure_time")


class OrderAdminTests(AdminSiteTestCase):
    """Test cases for Order admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = OrderAdmin(Order, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(
            self.admin.list_display,
            ("created_at", "customer", "tickets_count"),
        )

    def test_list_filter(self) -> None:
        """Test list_filter settings."""
        self.assertEqual(
            self.admin.list_filter,
            ("created_at", "user"),
        )

    def test_search_fields(self) -> None:
        """Test search_fields settings."""
        self.assertEqual(
            self.admin.search_fields,
            ("user__email", "user__first_name", "user__last_name"),
        )

    def test_date_hierarchy(self) -> None:
        """Test date_hierarchy setting."""
        self.assertEqual(self.admin.date_hierarchy, "created_at")

    def test_customer_method(self) -> None:
        """Test customer method returns full name."""
        self.assertEqual(
            self.admin.customer(self.order),
            self.user.get_full_name(),
        )

    def test_tickets_count_method(self) -> None:
        """Test tickets_count method returns correct count."""
        self.assertEqual(self.admin.tickets_count(self.order), 1)

        Ticket.objects.create(
            row=1,
            seat=2,
            flight=self.flight,
            order=self.order,
        )
        self.assertEqual(self.admin.tickets_count(self.order), 2)

    def test_get_queryset(self) -> None:
        """Test get_queryset method optimizes database queries."""
        request = self.client.get("/").wsgi_request
        queryset = self.admin.get_queryset(request)

        self.assertTrue("user" in queryset.query.select_related)


class TicketAdminTests(AdminSiteTestCase):
    """Test cases for Ticket admin interface."""
    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.admin = TicketAdmin(Ticket, self.site)

    def test_list_display(self) -> None:
        """Test list_display settings."""
        self.assertEqual(
            self.admin.list_display,
            ("flight", "seat_number", "order"),
        )

    def test_list_filter(self) -> None:
        """Test list_filter settings."""
        self.assertEqual(
            self.admin.list_filter,
            (
                "flight__route__source",
                "flight__route__destination",
                "flight__departure_time",
            ),
        )

    def test_admin_filter_search(self) -> None:
        """Test filter and search functionality."""
        url = reverse("admin:airport_ticket_changelist")

        response = self.client.get(
            url,
            {"flight__route__source__id__exact": self.airport.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ticket.seat_number)

        response = self.client.get(url, {"q": str(self.ticket.flight)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ticket.seat_number)
