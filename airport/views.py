from django.db.models import Count
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
from airport.permissions import IsAdminOrReadCreateOnly
from airport.serializers import (
    AirplaneDetailSerializer,
    AirplaneImageSerializer,
    AirplaneListSerializer,
    AirplaneSerializer,
    AirplaneTypeListSerializer,
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
    Base viewset that provides default CRUD operations
    with custom permissions.
    """
    permission_classes = (IsAdminOrReadCreateOnly,)


class AirportViewSet(BaseViewSet):
    """ViewSet for Airport instances."""
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirplaneTypeViewSet(BaseViewSet):
    """ViewSet for AirplaneType instances."""
    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return AirplaneType.objects.annotate(airplanes_count=Count("airplanes"))
        return AirplaneType.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneTypeListSerializer
        return AirplaneTypeSerializer


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


class FlightViewSet(BaseViewSet):
    """ViewSet for Flight instances."""
    queryset = Flight.objects.select_related(
        "airplane",
        "airplane__airplane_type",
        "route__source",
        "route__destination",
        ).prefetch_related("crew")

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class OrderViewSet(BaseViewSet):
    """ViewSet for Order instances."""
    def get_queryset(self):
        if self.action == "list":
            return Order.objects.select_related("user").prefetch_related("tickets")
        if self.action == "retrieve":
            return Order.objects.select_related("user").prefetch_related(
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
                "tickets__flight__airplane__airplane_type",
                "tickets__flight__crew",
            )
        return Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """Save order with current user."""
        serializer.save(user=self.request.user)


class TicketViewSet(BaseViewSet):
    """ViewSet for Ticket instances."""
    def get_queryset(self):
        if self.action == "list":
            return Ticket.objects.select_related(
                "flight__route__source", "flight__route__destination", "order"
            )
        if self.action == "retrieve":
            return Ticket.objects.select_related(
                "flight__route__source",
                "flight__route__destination",
                "flight__airplane__airplane_type",
            )
        if not self.request.user.is_staff:
            return Ticket.objects.filter(order__user=self.request.user)
        return Ticket.objects.all()

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
