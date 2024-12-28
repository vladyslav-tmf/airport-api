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


class SearchableCharFilterMixin:
    """Mixin that adds case-insensitive search for char fields."""

    def get_search_fields(self) -> dict:
        """Get search fields."""
        return {
            field: filters.CharFilter(field_name=field, lookup_expr="icontains")
            for field in self.search_fields
        }


class RangeNumberFilterMixin:
    """Mixin that adds range filtering for number fields."""

    def get_range_fields(self) -> dict:
        """Get range fields."""
        range_filters = {}

        for field in self.range_fields:
            range_filters.update(
                {
                    field: filters.NumberFilter(field_name=field),
                    f"{field}__gt": filters.NumberFilter(
                        field_name=field, lookup_expr="gt"
                    ),
                    f"{field}__lt": filters.NumberFilter(
                        field_name=field, lookup_expr="lt"
                    ),
                }
            )

        return range_filters


class DateTimeRangeFilterMixin:
    """Mixin that adds range filtering for datetime fields."""

    def get_datetime_range_fields(self) -> dict:
        """Get datetime range fields."""
        range_filters = {}

        for field in self.datetime_fields:
            field_name = field
            range_filters.update(
                {
                    field_name: filters.DateTimeFilter(field_name=field_name),
                    f"{field_name}__gt": filters.DateTimeFilter(
                        field_name=field_name, lookup_expr="gt"
                    ),
                    f"{field_name}__lt": filters.DateTimeFilter(
                        field_name=field_name, lookup_expr="lt"
                    ),
                }
            )

        return range_filters


class AirportFilter(filters.FilterSet, SearchableCharFilterMixin):
    """FilterSet for Airport model."""

    search_fields = ("name", "closest_big_city")

    class Meta:
        model = Airport
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(self.get_search_fields())


class AirplaneTypeFilter(filters.FilterSet, SearchableCharFilterMixin):
    """FilterSet for AirplaneType model."""

    search_fields = ("name",)

    class Meta:
        model = AirplaneType
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(self.get_search_fields())


class AirplaneFilter(
    filters.FilterSet,
    SearchableCharFilterMixin,
    RangeNumberFilterMixin,
):
    """FilterSet for Airplane model."""

    search_fields = ("name",)
    range_fields = ("rows", "seats_in_row")

    class Meta:
        model = Airplane
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(
            self.get_search_fields(),
            airplane_type_name=filters.CharFilter(
                field_name="airplane_type__name", lookup_expr="icontains"
            ),
            **self.get_range_fields(),
        )


class CrewFilter(filters.FilterSet, SearchableCharFilterMixin):
    """FilterSet for Crew model."""

    search_fields = ("first_name", "last_name")

    class Meta:
        model = Crew
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(self.get_search_fields())


class RouteFilter(filters.FilterSet, SearchableCharFilterMixin, RangeNumberFilterMixin):
    """FilterSet for Route model."""

    search_fields = ()
    range_fields = ("distance",)

    class Meta:
        model = Route
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(
            source_name=filters.CharFilter(
                field_name="source__name", lookup_expr="icontains"
            ),
            destination_name=filters.CharFilter(
                field_name="destination__name", lookup_expr="icontains"
            ),
            **self.get_range_fields(),
        )


class FlightFilter(
    filters.FilterSet, SearchableCharFilterMixin, DateTimeRangeFilterMixin
):
    """FilterSet for Flight model."""

    search_fields = ()
    datetime_fields = ("departure_time", "arrival_time")

    class Meta:
        model = Flight
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(
            route_source_name=filters.CharFilter(
                field_name="route__source__name", lookup_expr="icontains"
            ),
            route_destination_name=filters.CharFilter(
                field_name="route__destination__name", lookup_expr="icontains"
            ),
            **self.get_datetime_range_fields(),
        )


class OrderFilter(filters.FilterSet, DateTimeRangeFilterMixin):
    """FilterSet for Order model."""

    datetime_fields = ("created_at",)

    class Meta:
        model = Order
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(self.get_datetime_range_fields())


class TicketFilter(filters.FilterSet, RangeNumberFilterMixin):
    """FilterSet for Ticket model."""

    range_fields = ("row", "seat")

    class Meta:
        model = Ticket
        fields = ()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.filters.update(
            flight_route_source_name=filters.CharFilter(
                field_name="flight__route__source__name", lookup_expr="icontains"
            ),
            flight_route_destination_name=filters.CharFilter(
                field_name="flight__route__destination__name", lookup_expr="icontains"
            ),
            **self.get_range_fields(),
        )
