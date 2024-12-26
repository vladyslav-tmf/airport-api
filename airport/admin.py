from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

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


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "closest_big_city")
    list_filter = ("closest_big_city",)
    search_fields = ("name", "closest_big_city")


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "airplane_type", "rows", "seats_in_row", "total_seats")
    list_filter = ("airplane_type",)
    search_fields = ("name", "airplane_type__name")


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance")
    list_filter = ("source", "destination")
    search_fields = ("source__name", "destination__name")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "airplane",
        "departure_time",
        "arrival_time",
        "available_seats",
    )
    list_filter = ("route__source", "route__destination", "departure_time", "crew")
    search_fields = (
        "route__source__name",
        "route__source__closest_big_city",
        "route__destination__name",
        "route__destination__closest_big_city",
        "airplane__name",
    )
    date_hierarchy = "departure_time"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "customer", "tickets_count")
    list_filter = ("created_at", "user")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    date_hierarchy = "created_at"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Order]:
        """Optimize database queries by using select_related for the user field."""
        return super().get_queryset(request).select_related("user")

    def customer(self, order: Order) -> str:
        """Get customer full name by combining first and last name."""
        return order.user.get_full_name()

    def tickets_count(self, order: Order) -> int:
        """Get total number of tickets in the order."""
        return order.tickets.count()


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("flight", "seat_number", "order")
    list_filter = (
        "flight__route__source",
        "flight__route__destination",
        "flight__departure_time",
    )
