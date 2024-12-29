from django.core.cache import cache
from django.db.models.signals import post_delete, post_save

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


CACHE_KEYS_MAPPING = {
    Airport: ("airport_view", "route_view", "flight_view", "ticket_view"),
    AirplaneType: ("airplane_type_view", "flight_view", "airplane_view"),
    Airplane: ("airplane_view", "flight_view"),
    Crew: ("crew_view", "flight_view"),
    Route: ("route_view", "flight_view", "ticket_view"),
    Flight: ("flight_view", "crew_view"),
    Order: ("order_view", "ticket_view"),
    Ticket: ("ticket_view", "flight_view", "order_view"),
}

def invalidate_related_caches(sender: type, **kwargs) -> None:
    """
    Generic cache invalidation function that uses the mapping to determine
    which cache keys to invalidate for a given model.
    """
    if sender in CACHE_KEYS_MAPPING:
        for key_pattern in CACHE_KEYS_MAPPING[sender]:
            cache.delete_pattern(f"*{key_pattern}*")


for model in CACHE_KEYS_MAPPING:
    for signal in (post_save, post_delete):
        signal.connect(invalidate_related_caches, sender=model)
