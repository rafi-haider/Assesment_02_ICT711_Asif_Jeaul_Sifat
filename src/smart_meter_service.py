import random
import uuid
from datetime import datetime


def generate_meter_event(user_id, user_type):
    """
    Emulates the ingestion of smart meter IoT data.

    A solar energy generator supplies electricity to a seller.
    A consumer uses electricity from the electricity network.
    """

    if user_type not in ["seller", "buyer"]:
        raise ValueError("user_type must be either 'seller' or 'buyer'")

    energy_kwh = round(random.uniform(1.0, 10.0), 2)

    if user_type == "seller":
        event_type = "EnergyGeneratedEvent"
    else:
        event_type = "EnergyConsumedEvent"

    return {
        "event_type": event_type,
        "user_id": user_id,
        "user_type": user_type,
        "energy_kwh": energy_kwh,
        "timestamp": datetime.now().isoformat(),
        "correlation_id": str(uuid.uuid4())
    }


def generate_multiple_meter_events(number_of_events):
    """
    Simulates high-frequency IoT meter data by generating multiple events.
    """

    events = []

    for i in range(number_of_events):
        if i % 2 == 0:
            events.append(generate_meter_event(f"SELLER_{i + 1:03}", "seller"))
        else:
            events.append(generate_meter_event(f"BUYER_{i + 1:03}", "buyer"))

    return events
