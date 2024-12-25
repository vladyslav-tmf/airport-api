from uuid import UUID

from django.db.models import Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.utils import timezone
from rest_framework.viewsets import GenericViewSet

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
from airport.permissions import (
    IsAdminOrAuthenticatedCreateOnly,
    IsAdminOrAuthenticatedReadOnly,
    IsAdminOrReadOnly,
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


class BaseViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """
    Base viewset that provides default CRUD operations (except delete)
    with custom permissions.
    """
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all airports.",
        responses={
            status.HTTP_200_OK: AirportSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Airports",),
    ),
    create=extend_schema(
        description="Create a new airport.",
        request=AirportSerializer,
        responses={
            status.HTTP_201_CREATED: AirportSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to create an airport."
            ),
        },
        tags=("Airports",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific airport.",
        responses={
            status.HTTP_200_OK: AirportSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airport not found."
            ),
        },
        tags=("Airports",),
    ),
    update=extend_schema(
        description="Full update of airport information.",
        request=AirportSerializer,
        responses={
            status.HTTP_200_OK: AirportSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an airport."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airport not found."
            ),
        },
        tags=("Airports",),
    ),
    partial_update=extend_schema(
        description="Partial update of airport information.",
        request=AirportSerializer,
        responses={
            status.HTTP_200_OK: AirportSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an airport."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airport not found."
            ),
        },
        tags=("Airports",),
    ),
)
class AirportViewSet(BaseViewSet):
    """ViewSet for Airport instances."""
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all airplane types with count of airplanes.",
        responses={
            status.HTTP_200_OK: AirplaneTypeListRetrieveSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Airplane Types",),
    ),
    create=extend_schema(
        description="Create a new airplane type.",
        request=AirplaneTypeSerializer,
        responses={
            status.HTTP_201_CREATED: AirplaneTypeSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to create an airplane type."
            ),
        },
        tags=("Airplane Types",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific airplane type.",
        responses={
            status.HTTP_200_OK: AirplaneTypeListRetrieveSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airplane type not found."
            ),
        },
        tags=("Airplane Types",),
    ),
    update=extend_schema(
        description="Full update of airplane type information.",
        request=AirplaneTypeSerializer,
        responses={
            status.HTTP_200_OK: AirplaneTypeSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an airplane type."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airplane type not found."
            ),
        },
        tags=("Airplane Types",),
    ),
    partial_update=extend_schema(
        description="Partial update of airplane type information.",
        request=AirplaneTypeSerializer,
        responses={
            status.HTTP_200_OK: AirplaneTypeSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an airplane type."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airplane type not found."
            ),
        },
        tags=("Airplane Types",),
    ),
)
class AirplaneTypeViewSet(BaseViewSet):
    """ViewSet for AirplaneType instances."""
    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return AirplaneType.objects.annotate(airplanes_count=Count("airplanes"))

        return AirplaneType.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneTypeListRetrieveSerializer

        return AirplaneTypeSerializer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all airplanes.",
        responses={
            status.HTTP_200_OK: AirplaneListSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Airplanes",),
    ),
    create=extend_schema(
        description="Create a new airplane.",
        request=AirplaneSerializer,
        responses={
            status.HTTP_201_CREATED: AirplaneSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to create an airplane."
            ),
        },
        tags=("Airplanes",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific airplane.",
        responses={
            status.HTTP_200_OK: AirplaneDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airplane not found."
            ),
        },
        tags=("Airplanes",),
    ),
    update=extend_schema(
        description="Full update of airplane information.",
        request=AirplaneSerializer,
        responses={
            status.HTTP_200_OK: AirplaneSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an airplane."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airplane not found."
            ),
        },
        tags=("Airplanes",),
    ),
    partial_update=extend_schema(
        description="Partial update of airplane information.",
        request=AirplaneSerializer,
        responses={
            status.HTTP_200_OK: AirplaneSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an airplane."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airplane not found."
            ),
        },
        tags=("Airplanes",),
    ),
)
class AirplaneViewSet(BaseViewSet):
    """ViewSet for Airplane instances."""
    queryset = Airplane.objects.select_related("airplane_type")

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        if self.action == "retrieve":
            return AirplaneDetailSerializer

        if self.action == "upload_image":
            return AirplaneImageSerializer

        return AirplaneSerializer

    @extend_schema(
        description="Upload an image for a specific airplane.",
        request=AirplaneImageSerializer,
        responses={
            status.HTTP_200_OK: AirplaneImageSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid image provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an airplane."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Airplane not found."
            ),
        },
        tags=("Airplanes",),
    )
    @action(
        methods=("POST",),
        detail=True,
        url_path="upload-image",
        permission_classes=(IsAdminUser,)
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific airplane."""
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all crew members with their flight counts.",
        responses={
            status.HTTP_200_OK: CrewListSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Crew",),
    ),
    create=extend_schema(
        description="Create a new crew member.",
        request=CrewSerializer,
        responses={
            status.HTTP_201_CREATED: CrewSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to create a crew member."
            ),
        },
        tags=("Crew",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific crew member.",
        responses={
            status.HTTP_200_OK: CrewSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Crew member not found."
            ),
        },
        tags=("Crew",),
    ),
    update=extend_schema(
        description="Full update of crew member information.",
        request=CrewSerializer,
        responses={
            status.HTTP_200_OK: CrewSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a crew member."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Crew member not found."
            ),
        },
        tags=("Crew",),
    ),
    partial_update=extend_schema(
        description="Partial update of crew member information.",
        request=CrewSerializer,
        responses={
            status.HTTP_200_OK: CrewSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a crew member."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Crew member not found."
            ),
        },
        tags=("Crew",),
    ),
)
class CrewViewSet(BaseViewSet):
    """ViewSet for Crew instances."""
    def get_queryset(self):
        if self.action == "list":
            return Crew.objects.annotate(flights_count=Count("flights"))

        return Crew.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer

        return CrewSerializer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all routes.",
        responses={
            status.HTTP_200_OK: RouteListSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Routes",),
    ),
    create=extend_schema(
        description="Create a new route.",
        request=RouteSerializer,
        responses={
            status.HTTP_201_CREATED: RouteSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to create a route."
            ),
        },
        tags=("Routes",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific route.",
        responses={
            status.HTTP_200_OK: RouteDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Route not found."
            ),
        },
        tags=("Routes",),
    ),
    update=extend_schema(
        description="Full update of route information.",
        request=RouteSerializer,
        responses={
            status.HTTP_200_OK: RouteSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a route."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Route not found."),
        },
        tags=("Routes",),
    ),
    partial_update=extend_schema(
        description="Partial update of route information.",
        request=RouteSerializer,
        responses={
            status.HTTP_200_OK: RouteSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a route."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Route not found."),
        },
        tags=("Routes",),
    ),
)
class RouteViewSet(BaseViewSet):
    """ViewSet for Route instances."""
    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return Route.objects.select_related("source", "destination")

        return Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all flights with filtering options.",
        parameters=[
            OpenApiParameter(
                name="source_airport",
                type=OpenApiTypes.UUID,
                description="Filter by source airport ID.",
            ),
            OpenApiParameter(
                name="destination_airport",
                type=OpenApiTypes.UUID,
                description="Filter by destination airport ID.",
            ),
            OpenApiParameter(
                name="departure_date",
                type=OpenApiTypes.DATE,
                description="Filter by departure date (YYYY-MM-DD).",
            ),
            OpenApiParameter(
                name="crew",
                type=OpenApiTypes.STR,
                description="Filter by crew member IDs (comma separated UUIDs).",
            ),
            OpenApiParameter(
                name="airplane_type",
                type=OpenApiTypes.UUID,
                description="Filter by airplane type ID.",
            ),
        ],
        responses={status.HTTP_200_OK: FlightListSerializer},
        tags=("Flights",),
    ),
    create=extend_schema(
        description="Create a new flight.",
        request=FlightSerializer,
        responses={
            status.HTTP_201_CREATED: FlightSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to create a flight."
            ),
        },
        tags=("Flights",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific flight.",
        responses={
            status.HTTP_200_OK: FlightDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Flight not found."),
        },
        tags=("Flights",),
    ),
    update=extend_schema(
        description="Full update of flight information.",
        request=FlightSerializer,
        responses={
            status.HTTP_200_OK: FlightSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a flight."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Flight not found."),
        },
        tags=("Flights",),
    ),
    partial_update=extend_schema(
        description="Partial update of flight information.",
        request=FlightSerializer,
        responses={
            status.HTTP_200_OK: FlightSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a flight."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Flight not found."),
        },
        tags=("Flights",),
    ),
)
class FlightViewSet(BaseViewSet):
    """ViewSet for Flight instances with advanced filtering."""
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":

            return FlightListSerializer
        if self.action == "retrieve":

            return FlightDetailSerializer

        return FlightSerializer

    @staticmethod
    def _params_to_uuids(queryset):
        """Convert string of comma separated UUIDs to list of UUIDs."""
        try:
            return [UUID(str_id) for str_id in queryset.split(",")]

        except ValueError as error:
            raise serializers.ValidationError({"crew": f"Invalid UUID format: {error}"})

    def get_queryset(self):
        """
        Retrieve flights with filters:
        - source_airport: ID of source airport.
        - destination_airport: ID of destination airport.
        - departure_data: Date of departure.
        - crew: List of crew member IDs.
        - airplane_type: ID of airplane type.
        """
        queryset = Flight.objects.select_related(
            "airplane",
            "airplane__airplane_type",
            "route__source",
            "route__destination",
        ).prefetch_related("crew")

        source = self.request.query_params.get("source_airport")
        destination = self.request.query_params.get("destination_airport")
        departure_date = self.request.query_params.get("departure_date")
        crew = self.request.query_params.get("crew")
        airplane_type = self.request.query_params.get("airplane_type")

        if source:
            queryset = queryset.filter(route__source__id=source)

        if destination:
            queryset = queryset.filter(route__destination__id=destination)

        if departure_date:
            date = timezone.datetime.strptime(departure_date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=date)

        if crew:
            crew_ids = self._params_to_uuids(crew)
            queryset = queryset.filter(crew__id__in=crew_ids)

        if airplane_type:
            queryset = queryset.filter(airplane__airplane_type_id=airplane_type)

        return queryset.distinct()


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of user's orders.",
        responses={
            status.HTTP_200_OK: OrderListSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Orders",),
    ),
    create=extend_schema(
        description="Create a new order.",
        request=OrderSerializer,
        responses={
            status.HTTP_201_CREATED: OrderSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Orders",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific order.",
        responses={
            status.HTTP_200_OK: OrderDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Order not found."),
        },
        tags=("Orders",),
    ),
    update=extend_schema(
        description="Full update of order information.",
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OrderSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an order."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Order not found."),
        },
        tags=("Orders",),
    ),
    partial_update=extend_schema(
        description="Partial update of order information.",
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OrderSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update an order."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Order not found."),
        },
        tags=("Orders",),
    ),
)
class OrderViewSet(BaseViewSet):
    """ViewSet for Order instances."""
    permission_classes = (IsAdminOrAuthenticatedCreateOnly,)

    def get_queryset(self):
        queryset = Order.objects.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if self.action == "list":
            return queryset.select_related("user").prefetch_related("tickets")

        if self.action == "retrieve":
            return queryset.select_related("user").prefetch_related(
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
                "tickets__flight__airplane__airplane_type",
                "tickets__flight__crew",
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        """Save order with current user."""
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of user's tickets.",
        responses={
            status.HTTP_200_OK: TicketListSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
        },
        tags=("Tickets",),
    ),
    create=extend_schema(
        description="Create a new ticket.",
        request=TicketSerializer,
        responses={
            status.HTTP_201_CREATED: TicketSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
        },
        tags=("Tickets",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific ticket.",
        responses={
            status.HTTP_200_OK: TicketDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Ticket not found."),
        },
        tags=("Tickets",),
    ),
    update=extend_schema(
        description="Full update of ticket information.",
        request=TicketSerializer,
        responses={
            status.HTTP_200_OK: TicketSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a ticket."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Ticket not found."),
        },
        tags=("Tickets",),
    ),
    partial_update=extend_schema(
        description="Partial update of ticket information.",
        request=TicketSerializer,
        responses={
            status.HTTP_200_OK: TicketSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid data provided."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="User is not authenticated."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="User does not have permission to update a ticket."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Ticket not found."),
        },
        tags=("Tickets",),
    ),
)
class TicketViewSet(BaseViewSet):
    """ViewSet for Ticket instances."""
    permission_classes = (IsAdminOrAuthenticatedCreateOnly,)

    def get_queryset(self):
        queryset = Ticket.objects.all()

        if not self.request.user.is_staff:
            return queryset.filter(order__user=self.request.user)

        if self.action == "list":
            return queryset.select_related(
                "flight__route__source", "flight__route__destination", "order"
            )

        if self.action == "retrieve":
            return queryset.select_related(
                "flight__route__source",
                "flight__route__destination",
                "flight__airplane__airplane_type",
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer

        if self.action == "retrieve":
            return TicketDetailSerializer

        return TicketSerializer

    def perform_create(self, serializer):
        """Create ticket only for user's order."""
        order = serializer.validated_data["order"]

        if order.user != self.request.user:
            raise serializers.ValidationError(
                {"order": "You can't create tickets for other user orders"}
            )
