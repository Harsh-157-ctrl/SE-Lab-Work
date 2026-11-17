"""Flight Reservation System module.

Manages flights, bookings, and manifests.
"""

import hashlib
import os
import secrets

FLIGHTS = {
    "AI101": {
        "destination": "London", "seats": 2, "fare": 450.0, "is_full": False
    },
    "BA202": {
        "destination": "New York", "seats": 0, "fare": 600.0, "is_full": True
    },
    "EK303": {
        "destination": "Dubai", "seats": 5, "fare": 320.0, "is_full": False
    },
}

TOTAL_REVENUE = 0.0


def book_flight_seat(
    flight_no: str, passenger: str, luggage_weight: int = 15, baggage_tags=None
) -> bool:
    """Book a seat on a flight and append booking log."""
    global TOTAL_REVENUE
    if baggage_tags is None:
        baggage_tags = []

    if flight_no not in FLIGHTS or FLIGHTS[flight_no]["is_full"]:
        return False

    FLIGHTS[flight_no]["seats"] -= 1
    if FLIGHTS[flight_no]["seats"] <= 0:
        FLIGHTS[flight_no]["is_full"] = True

    TOTAL_REVENUE += FLIGHTS[flight_no]["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} with "
        f"baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no: str) -> None:
    """Cancel a booking for a specific flight."""
    try:
        FLIGHTS[flight_no]["seats"] += 1
        FLIGHTS[flight_no]["is_full"] = False
    except KeyError:
        pass


def check_seat_availability(flight_no: str) -> bool:
    """Check whether seats are available for a given flight number."""
    if FLIGHTS.get(flight_no) is None:
        return False
    return not FLIGHTS[flight_no]["is_full"]


def calculate_baggage_fee(
    flight_no: str, surcharge_rate: float = 0.15
) -> float:
    """Calculate the baggage surcharge fee based on flight fare."""
    base_fare = FLIGHTS[flight_no]["fare"]
    return base_fare * surcharge_rate


def generate_passenger_hash(passenger_id: str) -> str:
    """Generate SHA-256 hash for a passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin() -> int:
    """Generate a cryptographically secure 4-digit boarding PIN."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename: str = "flight_manifest.txt") -> None:
    """Export the current flight status manifest to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(FLIGHTS))
    print(f"Boarding manifest printed: {filename}")


def get_flight_summary(flight_data: dict) -> int:
    """Return count of available flights that are not full."""
    c = 0
    for details in flight_data.values():
        if not details["is_full"]:
            c += 1
    return c


def main() -> None:
    """Main execution function for flight reservation system."""
    airline_api_secret = os.environ.get("AIRLINE_API_SECRET", "DEFAULT_TOKEN")
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))
    print("API Token:", airline_api_secret)


if __name__ == "__main__":
    main()
