from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from accounts.admin import UserAdmin
from accounts.forms import CustomUserCreationForm
from airport.models import Order


User = get_user_model()


class UserAdminTests(TestCase):
    def setUp(self) -> None:
        """Set up test data."""
        self.site = AdminSite()
        self.admin = UserAdmin(User, self.site)
        self.client = Client()

        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        self.admin_user = User.objects.create_superuser(
            email="admin@test.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
        )

    def test_admin_login_required(self) -> None:
        """Test that admin page requires login."""
        response = self.client.get(reverse("admin:accounts_user_changelist"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/admin/login/?next={reverse('admin:accounts_user_changelist')}"
        )

        self.client.login(email="test@test.com", password="testpass123")
        response = self.client.get(reverse("admin:accounts_user_changelist"))
        self.assertEqual(response.status_code, 302)

        self.client.login(email="admin@test.com", password="adminpass123")
        response = self.client.get(reverse("admin:accounts_user_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_list_display(self) -> None:
        """Test that list_display contains correct fields."""
        self.assertIn("email", self.admin.list_display)
        self.assertIn("first_name", self.admin.list_display)
        self.assertIn("last_name", self.admin.list_display)
        self.assertIn("is_staff", self.admin.list_display)
        self.assertIn("orders_count", self.admin.list_display)

    def test_search_fields(self) -> None:
        """Test that search_fields contains correct fields."""
        self.assertIn("email", self.admin.search_fields)
        self.assertIn("first_name", self.admin.search_fields)
        self.assertIn("last_name", self.admin.search_fields)

    def test_ordering(self) -> None:
        """Test that ordering is set correctly."""
        self.assertEqual(self.admin.ordering, ("last_name", "first_name"))

    def test_fieldsets(self) -> None:
        """Test that fieldsets are configured correctly."""
        fieldsets = self.admin.fieldsets

        fieldset_names = [fieldset[0] for fieldset in fieldsets]
        self.assertIn(None, fieldset_names)
        self.assertIn("Personal info", fieldset_names)
        self.assertIn("Permissions", fieldset_names)
        self.assertIn("Important dates", fieldset_names)

        for fieldset in fieldsets:
            if not fieldset[0]:
                self.assertIn("email", fieldset[1]["fields"])
                self.assertIn("password", fieldset[1]["fields"])

            elif fieldset[0] == "Personal info":
                self.assertIn("first_name", fieldset[1]["fields"])
                self.assertIn("last_name", fieldset[1]["fields"])

            elif fieldset[0] == "Permissions":
                self.assertIn("is_active", fieldset[1]["fields"])
                self.assertIn("is_staff", fieldset[1]["fields"])
                self.assertIn("is_superuser", fieldset[1]["fields"])
                self.assertIn("groups", fieldset[1]["fields"])
                self.assertIn("user_permissions", fieldset[1]["fields"])

            elif fieldset[0] == "Important dates":
                self.assertIn("last_login", fieldset[1]["fields"])
                self.assertIn("date_joined", fieldset[1]["fields"])

    def test_add_fieldsets(self) -> None:
        """Test that add_fieldsets are configured correctly."""
        add_fieldsets = self.admin.add_fieldsets

        self.assertEqual(len(add_fieldsets), 1)
        self.assertIsNone(add_fieldsets[0][0])

        fields = add_fieldsets[0][1]["fields"]
        self.assertIn("email", fields)
        self.assertIn("first_name", fields)
        self.assertIn("last_name", fields)
        self.assertIn("password1", fields)
        self.assertIn("password2", fields)
        self.assertIn("wide", add_fieldsets[0][1]["classes"])

    def test_orders_count(self) -> None:
        """Test orders_count method returns correct count."""
        self.assertEqual(self.admin.orders_count(self.user), 0)

        Order.objects.create(user=self.user)
        Order.objects.create(user=self.user)

        self.assertEqual(self.admin.orders_count(self.user), 2)

    def test_add_form_configuration(self) -> None:
        """Test add form configuration."""
        self.assertEqual(self.admin.add_form, CustomUserCreationForm)
        self.assertIsNone(self.admin.add_form_template)
