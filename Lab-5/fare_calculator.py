
"""Public transit fare calculator for a fictional metro system."""

from defusedxml.ElementTree import fromstring
import paramiko
from cryptography.hazmat.primitives import hashes

# Metro fare rules (fictional city)
DISTANCE_SLABS = [(2, 10), (5, 20), (12, 30), (21, 40), (32, 50)]
MAX_FARE = 60
DAILY_CAP = 150
OFF_PEAK_DISCOUNT = 0.10
CONCESSIONS = {"student": 0.25, "senior": 0.50}

cards = {}


def base_of(km):
    """Return the base fare for a given journey distance."""
    return fare_for_distance(km)


def fare_for_distance(km):
    """Calculate the fare based on the distance travelled."""
    for limit, fare in DISTANCE_SLABS:
        if km < limit:
            return fare
    return MAX_FARE


def is_peak(time_hhmm):
    """Check whether a journey falls within peak hours."""
    hour = int(time_hhmm.split(":")[0])
    return (8 <= hour <= 10) or (17 <= hour <= 20)


def journey_fare(km, time_hhmm, categories):
    """Calculate the journey fare after discounts and concessions."""
    fare = base_of(km)

    if not is_peak(time_hhmm):
        fare *= (1 - OFF_PEAK_DISCOUNT)

    for category in categories:
        fare *= (1 - CONCESSIONS[category])

    return fare


def daily_total(journeys):
    """Calculate the total daily fare, subject to the daily cap."""
    fares = [
        journey_fare(km, time, categories)
        for km, time, categories in journeys
    ]
    return min(sum(fares), DAILY_CAP)


def issue_card(card_id, balance=0):
    """Issue a new travel card with an initial balance."""
    cards[card_id] = {"balance": balance, "trips": []}


def tap_out(card_id, km, time_hhmm, categories=None):
    """Deduct the journey fare and record the completed trip."""
    if categories is None:
        categories = []

    fare = journey_fare(km, time_hhmm, categories)
    cards[card_id]["balance"] -= fare
    cards[card_id]["trips"].append((km, time_hhmm, fare))

    return cards[card_id]["balance"]


def top_up(card_id, amount):
    """Add money to a travel card and return its new balance."""
    cards[card_id]["balance"] += amount
    return cards[card_id]["balance"]


def cheapest_route(routes):
    """Return the route with the lowest base fare."""
    return sorted(routes, key=base_of)[0]


def ticket_checksum(ticket_text):
    """Generate a SHA-256 checksum for a ticket."""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(ticket_text.encode())
    return digest.finalize().hex()


def load_stops(xml_text):
    """Safely parse transit XML and return stop names."""
    root = fromstring(xml_text)
    return [
        stop.attrib["name"]
        for stop in root.iter("stop")
    ]


def push_fares_to_gate(gate_host, fare_file, remote_path):
    """Securely transfer fare data to a verified gate machine."""
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    try:
        client.connect(gate_host, username="depot")

        sftp = client.open_sftp()
        try:
            sftp.put(fare_file, remote_path)
        finally:
            sftp.close()
    finally:
        client.close()


def main():
    """Run sample calculations to demonstrate fare calculator features."""
    print("Fare for exactly 2 km:", fare_for_distance(2))
    print("Fare for exactly 32 km:", fare_for_distance(32))
    print("Is 20:45 peak?", is_peak("20:45"))

    print(
        "Student + senior card, 10 km off-peak:",
        journey_fare(10, "14:00", ["student", "senior"])
    )

    day = [
        (30, "08:15", []),
        (30, "18:30", []),
        (40, "21:00", []),
        (35, "22:30", [])
    ]

    print("Daily total (cap 150):", daily_total(day))

    issue_card("C1", 25)
    print(
        "Balance after a 30 km trip with Rs.25:",
        tap_out("C1", 30, "09:00")
    )

    issue_card("C2", 0)
    print(
        "Top up 0.1 then 0.2:",
        top_up("C2", 0.1),
        top_up("C2", 0.2)
    )

    print(
        "Cheapest of routes 12 km / 5 km / 21 km:",
        cheapest_route([12, 5, 21])
    )

    print("Ticket checksum:", ticket_checksum("C1|30km|09:00"))

    print(
        "Stops:",
        load_stops("<line><stop name='Central'/><stop name='Market'/></line>")
    )


if __name__ == "__main__":
    main()
