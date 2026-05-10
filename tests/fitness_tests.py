import time
import sys
import os

# this Allows the test file to import modules from the src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from smart_meter_service import generate_meter_event
from marketplace_service import match_trade
from settlement_service import settle_payment


def test_event_processing_speed():
    """
    Fitness Function 1:
    Event processing must complete in less than 2 seconds.
    """

    start_time = time.time()

    seller = generate_meter_event("SELLER_TEST", "seller")
    buyer = generate_meter_event("BUYER_TEST", "buyer")
    trade = match_trade(seller, buyer)
    payment = settle_payment(trade)

    end_time = time.time()
    processing_time = end_time - start_time

    assert payment["status"] == "SUCCESS"
    assert processing_time < 2

    print("PASSED: Event processing completed under 2 seconds")


def test_invalid_payment_rejected():
    """
    Fitness Function 2:
    Invalid or negative payment amounts must be rejected.
    """

    invalid_trade = {
        "event_type": "TradeMatchedEvent",
        "seller_id": "SELLER_TEST",
        "buyer_id": "BUYER_TEST",
        "energy_kwh": 5,
        "price_per_kwh": 0.25,
        "total_price": -10,
        "correlation_id": "TEST-CORRELATION-ID"
    }

    payment = settle_payment(invalid_trade)

    assert payment["status"] == "FAILED"
    assert payment["event_type"] == "PaymentFailedEvent"

    print("PASSED: Invalid payment was rejected")


def test_trade_amount_is_correct():
    """
    Fitness Function 3:
    Marketplace must correctly match the smaller amount of available
    energy and buyer demand.
    """

    seller = {
        "event_type": "EnergyGeneratedEvent",
        "user_id": "SELLER_TEST",
        "user_type": "seller",
        "energy_kwh": 8,
        "correlation_id": "TEST-CORRELATION-ID"
    }

    buyer = {
        "event_type": "EnergyConsumedEvent",
        "user_id": "BUYER_TEST",
        "user_type": "buyer",
        "energy_kwh": 5,
        "correlation_id": "TEST-CORRELATION-ID"
    }

    trade = match_trade(seller, buyer)

    assert trade["energy_kwh"] == 5
    assert trade["total_price"] == 1.25

    print("PASSED: Trade matching and price calculation are correct")


def test_correlation_id_exists():
    """
    Fitness Function 4:
    Every generated smart meter event must include a correlation ID
    for observability and traceability.
    """

    event = generate_meter_event("SELLER_TEST", "seller")

    assert "correlation_id" in event
    assert event["correlation_id"] is not None
    assert len(event["correlation_id"]) > 0

    print("PASSED: Correlation ID exists in smart meter event")
