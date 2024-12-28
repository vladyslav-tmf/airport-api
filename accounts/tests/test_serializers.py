from django.test import TestCase
from rest_framework.exceptions import ValidationError

from accounts.serializers import UserSerializer
from accounts.tests.fixtures import DEFAULT_USER_DATA, INVALID_USER_DATA


class UserSerializerTests(TestCase):
    def setUp(self) -> None:
        """Set up test data."""
        self.user_data = DEFAULT_USER_DATA.copy()
        self.serializer = UserSerializer(data=self.user_data)
        self.assertTrue(self.serializer.is_valid())

    def test_contains_expected_fields(self) -> None:
        """Test that serializer contains expected fields."""
        user = self.serializer.save()
        data = UserSerializer(user).data

        self.assertCountEqual(
            data.keys(),
            ("id", "email", "first_name", "last_name", "is_staff"),
        )

    def test_password_write_only(self) -> None:
        """Test that password field is write-only."""
        self.assertNotIn("password", self.serializer.data)

    def test_password_validation(self) -> None:
        """Test password validation."""
        data = self.user_data
        data["password"] = "test"
        serializer = UserSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        data["password"] = "12345678"
        serializer = UserSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        data["password"] = "password123"
        serializer = UserSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_user(self) -> None:
        """Test creating user with valid data."""
        user = self.serializer.save()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertFalse(user.is_staff)

    def test_update_user(self) -> None:
        """Test updating user."""
        user = self.serializer.save()

        update_data = {
            "email": "updated@test.com",
            "password": "newpass123",
            "first_name": "Updated",
            "last_name": "Name",
        }
        serializer = UserSerializer(user, data=update_data)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, update_data["email"])
        self.assertTrue(updated_user.check_password(update_data["password"]))
        self.assertEqual(updated_user.first_name, update_data["first_name"])
        self.assertEqual(updated_user.last_name, update_data["last_name"])

    def test_update_user_partial(self) -> None:
        """Test partial update of user."""
        user = self.serializer.save()

        serializer = UserSerializer(user, data={"first_name": "NewName"}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.first_name, "NewName")
        self.assertEqual(updated_user.email, self.user_data["email"])
        self.assertEqual(updated_user.last_name, self.user_data["last_name"])
        self.assertTrue(updated_user.check_password(self.user_data["password"]))

    def test_read_only_fields(self) -> None:
        """Test read-only fields cannot be set."""
        data = self.user_data
        data["is_staff"] = True
        serializer = UserSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertFalse(user.is_staff)

    def test_email_validation(self) -> None:
        """Test email validation."""
        data = self.user_data
        data["email"] = "invalid-email"
        serializer = UserSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

        self.serializer.save()

        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_name_fields_validation(self) -> None:
        """Test first_name and last_name validation."""
        data = self.user_data
        data["first_name"] = ""
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

        data["first_name"] = "A" * 256
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

        data = self.user_data
        data["last_name"] = ""
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

        data["last_name"] = "A" * 256
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)

    def test_empty_fields_validation(self) -> None:
        """Test validation of empty required fields."""
        required_fields = ("email", "password", "first_name", "last_name")

        for field in required_fields:
            data = self.user_data
            data[field] = None
            serializer = UserSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_unique_email_on_update(self) -> None:
        """Test email uniqueness validation on update."""
        user1 = self.serializer.save()

        data = self.user_data
        data["email"] = "other@test.com"
        user2 = UserSerializer(data=data)
        self.assertTrue(user2.is_valid())
        user2 = user2.save()

        update_data = {"email": user1.email}
        serializer = UserSerializer(user2, data=update_data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_invalid_email_formats(self) -> None:
        """Test various invalid email formats."""
        invalid_emails = [
            "plainaddress",
            "@missinguser.com",
            "missing@domain",
            "spaces in@email.com",
            "test@test@test.com",
            "test.@test.com",
            ".test@test.com",
            "test..test@test.com",
            "test@test..com",
        ]

        for email in invalid_emails:
            data = self.user_data
            data["email"] = email
            serializer = UserSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("email", serializer.errors)

    def test_special_characters_in_names(self) -> None:
        """Test validation of special characters in name fields."""
        data = INVALID_USER_DATA["special_chars_name"]
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)

    def test_whitespace_only_names(self) -> None:
        """Test names containing only whitespace."""
        data = self.user_data
        data["first_name"] = "   "
        data["last_name"] = "   "
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)

    def test_password_common_patterns(self) -> None:
        """Test rejection of common password patterns."""
        common_patterns = [
            "qwerty123",
            "abc12345",
            "test1234",
            self.user_data["email"].split("@")[0] + "123",
        ]

        for password in common_patterns:
            data = self.user_data
            data["password"] = password
            serializer = UserSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("password", serializer.errors)
