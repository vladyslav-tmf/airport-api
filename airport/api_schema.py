from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from rest_framework import status


VALIDATION_400_RESPONSE = {
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid data provided.")
}

UNAUTHORIZED_401_RESPONSE = {
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        description="User is not authenticated."
    )
}

FORBIDDEN_403_RESPONSE = {
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        description="User does not have permission to perform this action."
    )
}

NOT_FOUND_404_RESPONSE = {
    status.HTTP_404_NOT_FOUND: OpenApiResponse(
        description="Requested object not found."
    )
}

SERVER_ERROR_500_RESPONSE = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        description="Internal server error."
    )
}

PAGINATION_PARAMETERS = [
    OpenApiParameter(
        name="page",
        type=OpenApiTypes.INT,
        description="Page number.",
        required=False,
    ),
    OpenApiParameter(
        name="page_size",
        type=OpenApiTypes.INT,
        description="Number of items per page (1-100).",
        required=False,
    ),
]

FLIGHT_FILTER_PARAMETERS = [
    OpenApiParameter(
        name="source_airport",
        type=OpenApiTypes.UUID,
        description="Filter by source airport ID.",
        required=False,
    ),
    OpenApiParameter(
        name="destination_airport",
        type=OpenApiTypes.UUID,
        description="Filter by destination airport ID.",
        required=False,
    ),
    OpenApiParameter(
        name="departure_date",
        type=OpenApiTypes.DATE,
        description="Filter by departure date (YYYY-MM-DD).",
        required=False,
    ),
    OpenApiParameter(
        name="crew",
        type=OpenApiTypes.STR,
        description="Filter by crew member IDs (comma separated UUIDs).",
        required=False,
    ),
    OpenApiParameter(
        name="airplane_type",
        type=OpenApiTypes.UUID,
        description="Filter by airplane type ID.",
        required=False,
    ),
]
