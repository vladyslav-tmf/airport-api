from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user_data = {
            "email": "test@test.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_create_user_success(self) -> None:
        """Test creating a user is successful."""
        response = self.client.post(
            reverse("accounts:user-create"),
            self.user_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertNotIn("password", response.data)

    def test_user_with_email_exists_error(self) -> None:
        """Test error returned if user with email exists."""
        User.objects.create_user(**self.user_data)
        response = self.client.post(
            reverse("accounts:user-create"),
            self.user_data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self) -> None:
        """Test an error is returned if password less than 8 chars."""
        payload = self.user_data.copy()
        payload["password"] = "test"
        response = self.client.post(
            reverse("accounts:user-create"),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_user_invalid_name_fields(self) -> None:
        """Test validation of first_name and last_name fields."""
        payload = self.user_data.copy()
        payload["first_name"] = ""
        response = self.client.post(
            reverse("accounts:user-create"),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload["first_name"] = "Test"
        payload["last_name"] = ""
        response = self.client.post(
            reverse("accounts:user-create"),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_success(self) -> None:
        """Test obtaining token for valid credentials."""
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            reverse("accounts:token-obtain-pair"),
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_obtain_token_bad_credentials(self) -> None:
        """Test returns error if credentials invalid."""
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            reverse("accounts:token-obtain-pair"),
            {
                "email": self.user_data["email"],
                "password": "wrongpass",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_protected_endpoint_unauthorized(self) -> None:
        """Test accessing protected endpoint without authentication."""
        response = self.client.get(reverse("accounts:user-manage"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self) -> None:
        """Test retrieving profile for logged in user."""
        response = self.client.get(reverse("accounts:user-manage"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)

    def test_post_me_endpoint_not_allowed(self) -> None:
        """Test POST is not allowed on me endpoint."""
        response = self.client.post(reverse("accounts:user-manage"), {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self) -> None:
        """Test updating the user profile for authenticated user."""
        payload = {
            "first_name": "Updated",
            "last_name": "Name",
            "password": "newpass123",
        }

        response = self.client.patch(reverse("accounts:user-manage"), payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, payload["last_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_user_profile(self) -> None:
        """Test partial update of user profile."""
        payload = {"first_name": "NewName"}
        response = self.client.patch(reverse("accounts:user-manage"), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, "User")

    def test_update_user_duplicate_email(self) -> None:
        """Test updating user with duplicate email."""
        User.objects.create_user(
            email="other@test.com",
            password="testpass123",
            first_name="Other",
            last_name="User",
        )
        payload = {"email": "other@test.com"}

        response = self.client.patch(reverse("accounts:user-manage"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "test@test.com")


class TokenBlacklistTests(TestCase):
    """Test token blacklist (logout) functionality."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.refresh = RefreshToken.for_user(self.user)

    def test_blacklist_token_success(self) -> None:
        """Test blacklisting token for logout."""
        response = self.client.post(
            reverse("accounts:token-blacklist"),
            {"refresh": str(self.refresh)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse("accounts:token-refresh"),
            {"refresh": str(self.refresh)},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_blacklist_token_invalid_token(self) -> None:
        """Test blacklisting invalid token returns error."""
        response = self.client.post(
            reverse("accounts:token-blacklist"),
            {"refresh": "invalid-token"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenRefreshTests(TestCase):
    """Test token refresh functionality."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.refresh = RefreshToken.for_user(self.user)

    def test_refresh_token_success(self) -> None:
        """Test refreshing token."""
        response = self.client.post(
            reverse("accounts:token-refresh"),
            {"refresh": str(self.refresh)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_invalid_token(self) -> None:
        """Test refreshing token with invalid refresh token."""
        response = self.client.post(
            reverse("accounts:token-refresh"),
            {"refresh": "invalid-token"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenVerifyTests(TestCase):
    """Test token verification functionality."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access = self.refresh.access_token

    def test_verify_token_success(self) -> None:
        """Test verifying valid token."""
        response = self.client.post(
            reverse("accounts:token-verify"),
            {"token": str(self.access)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token_invalid_token(self) -> None:
        """Test verifying invalid token."""
        response = self.client.post(
            reverse("accounts:token-verify"),
            {"token": "invalid-token"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
