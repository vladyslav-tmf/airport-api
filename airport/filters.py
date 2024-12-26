from django_filters import rest_framework as filters

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


class AirportFilter(filters.FilterSet):
    """FilterSet for Airport model."""

    name = filters.CharFilter(lookup_expr="icontains")
    closest_big_city = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Airport
        fields = ("name", "closest_big_city")


class AirplaneTypeFilter(filters.FilterSet):
    """FilterSet for AirplaneType model."""

    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = AirplaneType
        fields = ("name",)


class AirplaneFilter(filters.FilterSet):
    """FilterSet for Airplane model."""

    name = filters.CharFilter(lookup_expr="icontains")
    airplane_type_name = filters.CharFilter(
        field_name="airplane_type__name", lookup_expr="icontains"
    )
    rows = filters.NumberFilter()
    rows__gt = filters.NumberFilter(field_name="rows", lookup_expr="gt")
    rows__lt = filters.NumberFilter(field_name="rows", lookup_expr="lt")
    seats_in_row = filters.NumberFilter()
    seats_in_row__gt = filters.NumberFilter(field_name="seats_in_row", lookup_expr="gt")
    seats_in_row__lt = filters.NumberFilter(field_name="seats_in_row", lookup_expr="lt")

    class Meta:
        model = Airplane
        fields = (
            "name",
            "airplane_type_name",
            "rows",
            "rows__gt",
            "rows__lt",
            "seats_in_row",
            "seats_in_row__gt",
            "seats_in_row__lt",
        )


class CrewFilter(filters.FilterSet):
    """FilterSet for Crew model."""

    first_name = filters.CharFilter(lookup_expr="icontains")
    last_name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Crew
        fields = ("first_name", "last_name")


class RouteFilter(filters.FilterSet):
    """FilterSet for Route model."""

    source_name = filters.CharFilter(field_name="source__name", lookup_expr="icontains")
    destination_name = filters.CharFilter(
        field_name="destination__name", lookup_expr="icontains"
    )
    distance = filters.NumberFilter()
    distance__gt = filters.NumberFilter(field_name="distance", lookup_expr="gt")
    distance__lt = filters.NumberFilter(field_name="distance", lookup_expr="lt")

    class Meta:
        model = Route
        fields = (
            "source_name",
            "destination_name",
            "distance",
            "distance__gt",
            "distance__lt",
        )


class FlightFilter(filters.FilterSet):
    """FilterSet for Flight model."""

    route_source_name = filters.CharFilter(
        field_name="route__source__name", lookup_expr="icontains"
    )
    route_destination_name = filters.CharFilter(
        field_name="route__destination__name", lookup_expr="icontains"
    )
    departure_time = filters.DateTimeFilter()
    departure_time__gt = filters.DateTimeFilter(
        field_name="departure_time", lookup_expr="gt"
    )
    departure_time__lt = filters.DateTimeFilter(
        field_name="departure_time", lookup_expr="lt"
    )
    arrival_time = filters.DateTimeFilter()
    arrival_time__gt = filters.DateTimeFilter(
        field_name="arrival_time", lookup_expr="gt"
    )
    arrival_time__lt = filters.DateTimeFilter(
        field_name="arrival_time", lookup_expr="lt"
    )

    class Meta:
        model = Flight
        fields = (
            "route_source_name",
            "route_destination_name",
            "departure_time",
            "departure_time__gt",
            "departure_time__lt",
            "arrival_time",
            "arrival_time__gt",
            "arrival_time__lt",
        )


class OrderFilter(filters.FilterSet):
    """FilterSet for Order model."""

    created_at = filters.DateTimeFilter()
    created_at__gt = filters.DateTimeFilter(field_name="created_at", lookup_expr="gt")
    created_at__lt = filters.DateTimeFilter(field_name="created_at", lookup_expr="lt")

    class Meta:
        model = Order
        fields = ("created_at", "created_at__gt", "created_at__lt")


class TicketFilter(filters.FilterSet):
    """FilterSet for Ticket model."""

    flight_route_source_name = filters.CharFilter(
        field_name="flight__route__source__name", lookup_expr="icontains"
    )
    flight_route_destination_name = filters.CharFilter(
        field_name="flight__route__destination__name", lookup_expr="icontains"
    )
    row = filters.NumberFilter()
    row__gt = filters.NumberFilter(field_name="row", lookup_expr="gt")
    row__lt = filters.NumberFilter(field_name="row", lookup_expr="lt")
    seat = filters.NumberFilter()
    seat__gt = filters.NumberFilter(field_name="seat", lookup_expr="gt")
    seat__lt = filters.NumberFilter(field_name="seat", lookup_expr="lt")

    class Meta:
        model = Ticket
        fields = (
            "flight_route_source_name",
            "flight_route_destination_name",
            "row",
            "row__gt",
            "row__lt",
            "seat",
            "seat__gt",
            "seat__lt",
        )
