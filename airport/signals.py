from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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


@receiver((post_save, post_delete), sender=Airport)
def invalidate_airport_cache(
    sender: type[Airport],
    instance: Airport,
    **kwargs,
) -> None:
    """Invalidate cache when Airport instance is changed."""
    cache.delete_pattern("*airport_view*")


@receiver((post_save, post_delete), sender=AirplaneType)
def invalidate_airplane_type_cache(
    sender: type[AirplaneType],
    instance: AirplaneType,
    **kwargs,
) -> None:
    """Invalidate cache when AirplaneType instance is changed."""
    cache.delete_pattern("*airplane_type_view*")
    cache.delete_pattern("*flight_view*")


@receiver((post_save, post_delete), sender=Airplane)
def invalidate_airplane_cache(
    sender: type[Airplane],
    instance: Airplane,
    **kwargs,
) -> None:
    """Invalidate cache when Airplane instance is changed."""
    cache.delete_pattern("*airplane_view*")
    cache.delete_pattern("*flight_view*")


@receiver((post_save, post_delete), sender=Crew)
def invalidate_crew_cache(sender: type[Crew], instance: Crew, **kwargs) -> None:
    """Invalidate cache when Crew instance is changed."""
    cache.delete_pattern("*crew_view*")
    cache.delete_pattern("*flight_view*")


@receiver((post_save, post_delete), sender=Route)
def invalidate_route_cache(sender: type[Route], instance: Route, **kwargs) -> None:
    """Invalidate cache when Route instance is changed."""
    cache.delete_pattern("*route_view*")


@receiver((post_save, post_delete), sender=Flight)
def invalidate_flight_cache(sender: type[Flight], instance: Flight, **kwargs) -> None:
    """Invalidate cache when Flight instance is changed."""
    cache.delete_pattern("*flight_view*")
    cache.delete_pattern("*route_view*")


@receiver((post_save, post_delete), sender=Order)
def invalidate_order_cache(sender: type[Order], instance: Order, **kwargs) -> None:
    """Invalidate cache when Order instance is changed."""
    cache.delete_pattern("*order_view*")
    cache.delete_pattern("*ticket_view*")


@receiver((post_save, post_delete), sender=Ticket)
def invalidate_ticket_cache(sender: type[Ticket], instance: Ticket, **kwargs) -> None:
    """Invalidate cache when Ticket instance is changed."""
    cache.delete_pattern("*ticket_view*")
    cache.delete_pattern("*flight_view*")
