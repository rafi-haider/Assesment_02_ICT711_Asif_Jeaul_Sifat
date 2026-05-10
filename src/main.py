from event_stream import EventStream
from smart_meter_service import generate_meter_event, generate_multiple_meter_events
from marketplace_service import match_trade
from settlement_service import settle_payment
from observability import log_event


def run_single_trade_demo():
    """
    Runs one complete P2P energy trading flow.
    """

    print("\n========== ECOGRID ENERGY SINGLE TRADE DEMO ==========\n")

    event_stream = EventStream()

    seller_event = generate_meter_event("SELLER_001", "seller")
    buyer_event = generate_meter_event("BUYER_001", "buyer")

    event_stream.publish(seller_event)
    event_stream.publish(buyer_event)

    log_event(
        "SmartMeterService",
        "Smart meter events generated successfully",
        seller_event["correlation_id"]
    )

    trade_event = match_trade(seller_event, buyer_event)
    event_stream.publish(trade_event)

    log_event(
        "MarketplaceService",
        "Buyer and seller matched successfully",
        trade_event["correlation_id"]
    )

    payment_event = settle_payment(trade_event)
    event_stream.publish(payment_event)

    log_event(
        "SettlementService",
        "Payment settlement processed",
        payment_event["correlation_id"]
    )

    print("\n========== FINAL EVENT STREAM ==========\n")

    for event in event_stream.get_all_events():
        print(event)


def run_high_frequency_iot_demo():
    """
    Simulates high-frequency smart meter event generation.
    """

    print("\n========== HIGH-FREQUENCY IOT EVENT DEMO ==========\n")

    event_stream = EventStream()
    meter_events = generate_multiple_meter_events(10)

    for event in meter_events:
        event_stream.publish(event)

    generated_events = event_stream.get_events_by_type("EnergyGeneratedEvent")
    consumed_events = event_stream.get_events_by_type("EnergyConsumedEvent")

    print("\nTotal events generated:", len(event_stream.get_all_events()))
    print("Total seller energy events:", len(generated_events))
    print("Total buyer consumption events:", len(consumed_events))


if __name__ == "__main__":
    run_single_trade_demo()
    run_high_frequency_iot_demo()
