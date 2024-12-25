from uuid import UUID

from django.db.models import Count, QuerySet
from drf_spectacular.utils import (
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
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import timezone
from rest_framework.viewsets import GenericViewSet

from airport.api_schema import (
    FLIGHT_FILTER_PARAMETERS,
    FORBIDDEN_403_RESPONSE,
    NOT_FOUND_404_RESPONSE,
    PAGINATION_PARAMETERS,
    UNAUTHORIZED_401_RESPONSE,
    VALIDATION_400_RESPONSE,
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
            status.HTTP_200_OK: OpenApiResponse(
                response=AirportSerializer(many=True),
                description="Successfully retrieved list of airports.",
            ),
            **FORBIDDEN_403_RESPONSE,
        },
        tags=("Airports",),
    ),
    create=extend_schema(
        description="Create a new airport.",
        request=AirportSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=AirportSerializer,
                description="Successfully created airport.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
        },
        tags=("Airports",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific airport.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirportSerializer,
                description="Successfully retrieved airport.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airports",),
    ),
    update=extend_schema(
        description="Full update of airport information.",
        request=AirportSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirportSerializer,
                description="Successfully updated airport.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airports",),
    ),
    partial_update=extend_schema(
        description="Partial update of airport information.",
        request=AirportSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirportSerializer,
                description="Successfully updated airport.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airports",),
    ),
)
class AirportViewSet(BaseViewSet):
    """ViewSet for Airport instances."""
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = None


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all airplane types with count of airplanes.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneTypeListRetrieveSerializer(many=True),
                description="Successfully retrieved list of airplane types.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
        },
        tags=("Airplane Types",),
    ),
    create=extend_schema(
        description="Create a new airplane type.",
        request=AirplaneTypeSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=AirplaneTypeSerializer,
                description="Successfully created airplane type.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
        },
        tags=("Airplane Types",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific airplane type.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneTypeListRetrieveSerializer,
                description="Successfully retrieved airplane type.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airplane Types",),
    ),
    update=extend_schema(
        description="Full update of airplane type information.",
        request=AirplaneTypeSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneTypeSerializer,
                description="Successfully updated airplane type.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airplane Types",),
    ),
    partial_update=extend_schema(
        description="Partial update of airplane type information.",
        request=AirplaneTypeSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneTypeSerializer,
                description="Successfully updated airplane type.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airplane Types",),
    ),
)
class AirplaneTypeViewSet(BaseViewSet):
    """ViewSet for AirplaneType instances."""
    pagination_class = None

    def get_queryset(self) -> QuerySet[AirplaneType]:
        if self.action in ("list", "retrieve"):
            return AirplaneType.objects.annotate(airplanes_count=Count("airplanes"))

        return AirplaneType.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneTypeListRetrieveSerializer

        return AirplaneTypeSerializer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a paginated list of all airplanes.",
        parameters=PAGINATION_PARAMETERS,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneListSerializer(many=True),
                description="Successfully retrieved list of airplanes.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
        },
        tags=("Airplanes",),
    ),
    create=extend_schema(
        description="Create a new airplane.",
        request=AirplaneSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=AirplaneSerializer,
                description="Successfully created airplane.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
        },
        tags=("Airplanes",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific airplane.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneDetailSerializer,
                description="Successfully retrieved airplane.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airplanes",),
    ),
    update=extend_schema(
        description="Full update of airplane information.",
        request=AirplaneSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneSerializer,
                description="Successfully updated airplane.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airplanes",),
    ),
    partial_update=extend_schema(
        description="Partial update of airplane information.",
        request=AirplaneSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneSerializer,
                description="Successfully updated airplane.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
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
            status.HTTP_200_OK: OpenApiResponse(
                response=AirplaneImageSerializer,
                description="Successfully uploaded image.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Airplanes",),
    )
    @action(
        methods=("POST",),
        detail=True,
        url_path="upload-image",
        permission_classes=(IsAdminUser,)
    )
    def upload_image(self, request: Request, pk=None) -> Response:
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
            status.HTTP_200_OK: OpenApiResponse(
                response=CrewSerializer(many=True),
                description="Successfully retrieved list of crew members.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
        },
        tags=("Crew",),
    ),
    create=extend_schema(
        description="Create a new crew member.",
        request=CrewSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CrewSerializer,
                description="Successfully created crew member.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
        },
        tags=("Crew",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific crew member.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=CrewSerializer,
                description="Successfully retrieved crew member.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Crew",),
    ),
    update=extend_schema(
        description="Full update of crew member information.",
        request=CrewSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=CrewSerializer,
                description="Successfully updated crew member.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Crew",),
    ),
    partial_update=extend_schema(
        description="Partial update of crew member information.",
        request=CrewSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=CrewSerializer,
                description="Successfully updated crew member.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Crew",),
    ),
)
class CrewViewSet(BaseViewSet):
    """ViewSet for Crew instances."""
    pagination_class = None

    def get_queryset(self) -> QuerySet[Crew]:
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
            status.HTTP_200_OK: OpenApiResponse(
                response=RouteSerializer(many=True),
                description="Successfully retrieved list of routes.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
        },
        tags=("Routes",),
    ),
    create=extend_schema(
        description="Create a new route.",
        request=RouteSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=RouteSerializer,
                description="Successfully created route.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
        },
        tags=("Routes",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific route.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=RouteDetailSerializer,
                description="Successfully retrieved route.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Routes",),
    ),
    update=extend_schema(
        description="Full update of route information.",
        request=RouteSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=RouteSerializer,
                description="Successfully updated route.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Routes",),
    ),
    partial_update=extend_schema(
        description="Partial update of route information.",
        request=RouteSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=RouteSerializer,
                description="Successfully updated route.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Routes",),
    ),
)
class RouteViewSet(BaseViewSet):
    """ViewSet for Route instances."""
    pagination_class = None

    def get_queryset(self) -> QuerySet[Route]:
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
        description="Retrieve a paginated list of all flights with filtering options.",
        parameters=[
            *PAGINATION_PARAMETERS,
            *FLIGHT_FILTER_PARAMETERS,
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=FlightListSerializer(many=True),
                description="Flights successfully retrieved.",
            )
        },
        tags=("Flights",),
    ),
    create=extend_schema(
        description="Create a new flight.",
        request=FlightSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=FlightSerializer,
                description="Successfully created flight.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
        },
        tags=("Flights",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific flight.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=FlightDetailSerializer,
                description="Successfully retrieved flight.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Flights",),
    ),
    update=extend_schema(
        description="Full update of flight information.",
        request=FlightSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=FlightSerializer,
                description="Successfully updated flight.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Flights",),
    ),
    partial_update=extend_schema(
        description="Partial update of flight information.",
        request=FlightSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=FlightSerializer,
                description="Successfully updated flight.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
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
    def _params_to_uuids(params_string: str) -> list[UUID]:
        """Convert string of comma separated UUIDs to list of UUIDs."""
        try:
            return [UUID(str_id) for str_id in params_string.split(",")]

        except ValueError as error:
            raise serializers.ValidationError({"crew": f"Invalid UUID format: {error}"})

    def get_queryset(self) -> QuerySet[Flight]:
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
        description="Retrieve a paginated list of user's orders.",
        parameters=PAGINATION_PARAMETERS,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=OrderListSerializer(many=True),
                description="List of orders successfully retrieved.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
        },
        tags=("Orders",),
    ),
    create=extend_schema(
        description="Create a new order with tickets.",
        request=OrderSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=OrderSerializer,
                description="Successfully created order with tickets.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
        },
        tags=("Orders",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific order.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=OrderDetailSerializer,
                description="Order successfully retrieved.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Orders",),
    ),
    update=extend_schema(
        description="Full update of order information.",
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=OrderSerializer,
                description="Successfully updated order.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Orders",),
    ),
    partial_update=extend_schema(
        description="Partial update of order information.",
        request=OrderSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=OrderSerializer,
                description="Successfully updated order.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Orders",),
    ),
)
class OrderViewSet(BaseViewSet):
    """ViewSet for Order instances."""
    permission_classes = (IsAdminOrAuthenticatedCreateOnly,)

    def get_queryset(self) -> QuerySet[Order]:
        queryset = Order.objects.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if self.action == "list":
            return queryset.select_related("user").prefetch_related(
                "tickets"
            ).distinct()

        if self.action == "retrieve":
            return queryset.select_related("user").prefetch_related(
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
                "tickets__flight__airplane__airplane_type",
                "tickets__flight__crew",
            ).distinct()

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializer

    def perform_create(self, serializer: OrderSerializer) -> None:
        """Create order with tickets for current user."""
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a paginated list of user's tickets.",
        parameters=PAGINATION_PARAMETERS,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TicketListSerializer(many=True),
                description="List of tickets successfully retrieved.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
        },
        tags=("Tickets",),
    ),
    create=extend_schema(
        description="Create a new ticket.",
        request=TicketSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=TicketSerializer,
                description="Successfully created ticket.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **VALIDATION_400_RESPONSE,
        },
        tags=("Tickets",),
    ),
    retrieve=extend_schema(
        description="Get detailed information about a specific ticket.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TicketDetailSerializer,
                description="Ticket successfully retrieved.",
            ),
            **UNAUTHORIZED_401_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Tickets",),
    ),
    update=extend_schema(
        description="Full update of ticket information.",
        request=TicketSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TicketSerializer,
                description="Successfully updated ticket.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Tickets",),
    ),
    partial_update=extend_schema(
        description="Partial update of ticket information.",
        request=TicketSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TicketSerializer,
                description="Successfully updated ticket.",
            ),
            **VALIDATION_400_RESPONSE,
            **UNAUTHORIZED_401_RESPONSE,
            **FORBIDDEN_403_RESPONSE,
            **NOT_FOUND_404_RESPONSE,
        },
        tags=("Tickets",),
    ),
)
class TicketViewSet(BaseViewSet):
    """ViewSet for Ticket instances."""
    permission_classes = (IsAdminOrAuthenticatedCreateOnly,)

    def get_queryset(self) -> QuerySet[Ticket]:
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

    def perform_create(self, serializer: TicketSerializer) -> None:
        """Create ticket only for user's order."""
        order = serializer.validated_data["order"]

        if order.user != self.request.user:
            raise serializers.ValidationError(
                {"order": "You can't create tickets for other user orders"}
            )
