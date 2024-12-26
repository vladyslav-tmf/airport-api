from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

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


class AirportSerializer(serializers.ModelSerializer):
    """Serializer for Airport model."""

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    """Serializer for AirplaneType model."""

    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneTypeListRetrieveSerializer(AirplaneTypeSerializer):
    """Serializer for listing AirplaneType instances with count of related airplanes."""

    airplanes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = AirplaneType
        fields = ("id", "name", "airplanes_count")


class AirplaneSerializer(serializers.ModelSerializer):
    """Serializer for Airplane model."""

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "total_seats",
            "airplane_type",
            "image",
        )


class AirplaneListSerializer(serializers.ModelSerializer):
    """Serializer for listing Airplane instances with airplane type name."""

    airplane_type_name = serializers.CharField(
        source="airplane_type.name", read_only=True
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "total_seats",
            "airplane_type_name",
            "image",
        )


class AirplaneDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Airplane information including airplane type details."""

    airplane_type = AirplaneTypeListRetrieveSerializer(read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "total_seats",
            "airplane_type",
            "image",
        )


class AirplaneImageSerializer(serializers.ModelSerializer):
    """Serializer for Airplane image upload."""

    class Meta:
        model = Airplane
        fields = ("id", "image")


class CrewSerializer(serializers.ModelSerializer):
    """Serializer for Crew model."""

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class CrewListSerializer(serializers.ModelSerializer):
    """Serializer for listing Crew members with count of their flights."""

    flights_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Crew
        fields = ("id", "full_name", "flights_count")


class RouteSerializer(serializers.ModelSerializer):
    """Serializer for Route model with validation."""

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, attrs):
        """
        Validate route data:
        - Source and destination airports must be different.
        - Distance cannot exceed 20,000 km.
        """
        if attrs["source"] == attrs["destination"]:
            raise serializers.ValidationError(
                {"destination": "Source and destination airports cannot be the same"}
            )
        if attrs["distance"] > 20000:
            raise serializers.ValidationError(
                {"distance": "Distance cannot exceed 20,000 km"}
            )
        return attrs


class RouteListSerializer(serializers.ModelSerializer):
    """Serializer for listing Routes with source and destination airport names."""

    source_name = serializers.CharField(source="source.name", read_only=True)
    destination_name = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source_name", "destination_name", "distance")


class RouteDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Route information including full airport details."""

    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    """Serializer for Flight model with time validation."""

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "available_seats",
            "crew",
        )

    def validate(self, attrs):
        """Validate that arrival time is after departure time."""
        if attrs["arrival_time"] <= attrs["departure_time"]:
            raise serializers.ValidationError(
                {"arrival_time": "Arrival time must be after departure time"}
            )
        return attrs


class FlightListSerializer(serializers.ModelSerializer):
    """Serializer for listing Flights with related information."""

    source_airport = serializers.CharField(source="route.source.name", read_only=True)
    destination_airport = serializers.CharField(
        source="route.destination.name", read_only=True
    )
    airplane_name = serializers.CharField(source="airplane.name", read_only=True)
    crew_names = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "source_airport",
            "destination_airport",
            "airplane_name",
            "departure_time",
            "arrival_time",
            "available_seats",
            "crew_names",
        )

    def get_crew_names(self, flight):
        """Get list of full names of crew members assigned to the flight."""
        return [member.full_name for member in flight.crew.all()]


class FlightDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Flight information including related objects."""

    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)
    crew = CrewListSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "available_seats",
            "crew",
        )


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket model with seat and flight validation."""

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )

    def validate(self, attrs):
        """
        Validate ticket data:
        - Check if seat exists in airplane.
        - Check if flight is not in the past.
        """
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            serializers.ValidationError,
        )

        if attrs["flight"].departure_time <= timezone.now():
            raise serializers.ValidationError(
                {"flight": "Cannot create ticket for past flights"}
            )

        return attrs


class TicketListSerializer(serializers.ModelSerializer):
    """Serializer for listing Tickets with source and destination cities."""

    source_city = serializers.CharField(
        source="flight.route.source.closest_big_city", read_only=True
    )
    destination_city = serializers.CharField(
        source="flight.route.destination.closest_big_city", read_only=True
    )

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "seat_number",
            "source_city",
            "destination_city",
        )


class TicketDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Ticket information including flight details."""

    flight = FlightDetailSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
            "order",
        )


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model with nested tickets creation."""

    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data: dict) -> Order:
        """Create order with nested tickets in a single transaction."""
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)

            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

            return order


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for listing Orders with user and tickets information."""

    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    tickets_count = serializers.IntegerField(source="tickets.count", read_only=True)

    class Meta:
        model = Order
        fields = ("id", "user_full_name", "tickets_count", "created_at")


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Order information including user and tickets details."""

    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    tickets = TicketDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "user_full_name", "tickets", "created_at")
