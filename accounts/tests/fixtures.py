DEFAULT_USER_DATA = {
    "email": "test@test.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User",
}

INVALID_USER_DATA = {
    "invalid_email": {**DEFAULT_USER_DATA, "email": "not-an-email"},
    "short_password": {**DEFAULT_USER_DATA, "password": "short"},
    "numeric_password": {**DEFAULT_USER_DATA, "password": "12345678"},
    "common_password": {**DEFAULT_USER_DATA, "password": "password123"},
    "empty_first_name": {**DEFAULT_USER_DATA, "first_name": ""},
    "empty_last_name": {**DEFAULT_USER_DATA, "last_name": ""},
    "long_first_name": {**DEFAULT_USER_DATA, "first_name": "A" * 256},
    "long_last_name": {**DEFAULT_USER_DATA, "last_name": "A" * 256},
    "special_chars_name": {
        **DEFAULT_USER_DATA,
        "first_name": "Test@#$%",
        "last_name": "User@#$%",
    },
}
