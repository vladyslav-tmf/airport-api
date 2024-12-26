from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

from airport.utils import airplane_image_file_path
from base.models import TimestampedUUIDBaseModel


class Airport(TimestampedUUIDBaseModel):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} ({self.closest_big_city})"


class AirplaneType(TimestampedUUIDBaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Airplane(TimestampedUUIDBaseModel):
    name = models.CharField(max_length=255)
    rows = models.PositiveSmallIntegerField()
    seats_in_row = models.PositiveSmallIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )
    image = models.ImageField(null=True, blank=True, upload_to=airplane_image_file_path)

    @property
    def total_seats(self) -> int:
        """Calculate total number of seats in the airplane."""
        return self.rows * self.seats_in_row

    class Meta:
        ordering = ("airplane_type", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("name", "airplane_type"),
                name="unique_airplane_type_and_name",
            )
        ]

    def __str__(self) -> str:
        return f"{self.airplane_type.name} {self.name}"


class Crew(TimestampedUUIDBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self) -> str:
        """Get crew member's full name by combining first and last name."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name_plural = "crew"

    def __str__(self) -> str:
        return self.full_name


class Route(TimestampedUUIDBaseModel):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.PositiveSmallIntegerField(help_text="Distance in kilometers")

    class Meta:
        ordering = ("source", "destination")
        constraints = [
            UniqueConstraint(
                fields=("source", "destination"),
                name="unique_route",
            )
        ]

    def clean(self) -> None:
        if self.source == self.destination:
            raise ValidationError(
                {"destination": "Source and destination airports cannot be the same"}
            )

        if self.distance > 20000:
            raise ValidationError({"distance": "Distance cannot exceed 20,000 km"})

    def __str__(self) -> str:
        return f"{self.source.name} → {self.destination.name} ({self.distance} km)"


class Flight(TimestampedUUIDBaseModel):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    @property
    def available_seats(self) -> int:
        """Calculate number of available seats on the flight."""
        return self.airplane.total_seats - self.tickets.count()

    class Meta:
        ordering = ("departure_time",)

    def clean(self) -> None:
        if self.arrival_time <= self.departure_time:
            raise ValidationError(
                {"arrival_time": "Arrival time must be after departure time"}
            )

    def __str__(self) -> str:
        return (
            f"{self.route.source.name} "
            f"({self.departure_time.strftime('%Y.%m.%d %H:%M')}) → "
            f"{self.route.destination.name} "
            f"({self.arrival_time.strftime('%Y.%m.%d %H:%M')})"
        )


class Order(TimestampedUUIDBaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Order \"{self.id}\" by {self.user.get_full_name()}"


class Ticket(TimestampedUUIDBaseModel):
    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    @property
    def seat_number(self) -> str:
        """Get formatted seat number string combining row and seat numbers."""
        return f"{self.row}-{self.seat}"

    class Meta:
        ordering = ("flight",)
        constraints = [
            models.UniqueConstraint(
                fields=("flight", "row", "seat"),
                name="unique_flight_seat",
            )
        ]

    @staticmethod
    def validate_ticket(
        row: int,
        seat: int,
        airplane: Airplane,
        error_to_raise,
    ) -> None:
        """
        Validate that ticket row and seat numbers are within
        airplane's seating configuration.
        """
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: (
                            f"{ticket_attr_name} number must be in available range: "
                            f"(1, {airplane_attr_name}): (1, {count_attrs})"
                        )
                    }
                )

    def clean(self) -> None:
        self.validate_ticket(self.row, self.seat, self.flight.airplane, ValidationError)

        if self.flight.departure_time <= timezone.now():
            raise ValidationError({"flight": "Cannot create ticket for past flights"})

    def __str__(self) -> str:
        return (
            f"{self.flight.route.source.closest_big_city} → "
            f"{self.flight.route.destination.closest_big_city} "
            f"(Departure at {self.flight.departure_time.strftime("%Y.%m.%d %H:%M")}): "
            f"seat {self.row}-{self.seat}"
        )
