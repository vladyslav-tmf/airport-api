from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user(self):
        """Test creating a user with email."""
        user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin_user = User.objects.create_superuser(
            email="admin@test.com",
            password="testpass123",
            first_name="Admin",
            last_name="User",
        )

        self.assertEqual(admin_user.email, "admin@test.com")
        self.assertTrue(admin_user.check_password("testpass123"))
        self.assertEqual(admin_user.first_name, "Admin")
        self.assertEqual(admin_user.last_name, "User")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_user_without_email(self):
        """Test creating a user without email raises error."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="testpass123",
                first_name="Test",
                last_name="User",
            )

    def test_create_superuser_not_staff(self):
        """Test creating a superuser with is_staff=False raises error."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com",
                password="testpass123",
                first_name="Admin",
                last_name="User",
                is_staff=False,
            )

    def test_create_superuser_not_superuser(self):
        """Test creating a superuser with is_superuser=False raises error."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com",
                password="testpass123",
                first_name="Admin",
                last_name="User",
                is_superuser=False,
            )


class UserTests(TestCase):
    def setUp(self):
        """Create test user."""
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_user_str(self):
        """Test the user string representation."""
        self.assertEqual(
            str(self.user), f"{self.user.first_name} {self.user.last_name}"
        )

    def test_user_email_normalized(self):
        """Test email is normalized when creating user."""
        email = "test2@TEST.com"
        user = User.objects.create_user(
            email=email,
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.email, email.lower())

    def test_user_required_fields(self):
        """Test required fields are enforced."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="test3@test.com",
                password="testpass123",
                first_name="",
                last_name="User",
            )
