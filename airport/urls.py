from rest_framework import routers

from airport.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    CrewViewSet,
    FlightViewSet,
    OrderViewSet,
    RouteViewSet,
    TicketViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()
router.register("airport", AirportViewSet, basename="airport")
router.register("airplane-type", AirplaneTypeViewSet, basename="airplane-type")
router.register("airplane", AirplaneViewSet, basename="airplane")
router.register("crew", CrewViewSet, basename="crew")
router.register("route", RouteViewSet, basename="route")
router.register("flight", FlightViewSet, basename="flight")
router.register("order", OrderViewSet, basename="order")
router.register("ticket", TicketViewSet, basename="ticket")

urlpatterns = router.urls
