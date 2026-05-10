def settle_payment(trade_event):
    """
    Manages the financial part of a matched energy transaction.
    A basic security is demonstrated by refusing the invalid payments.
    fitness function.
    """

    if trade_event["total_price"] <= 0:
        return {
            "event_type": "PaymentFailedEvent",
            "status": "FAILED",
            "reason": "Invalid payment amount",
            "correlation_id": trade_event["correlation_id"]
        }

    return {
        "event_type": "PaymentSettledEvent",
        "seller_id": trade_event["seller_id"],
        "buyer_id": trade_event["buyer_id"],
        "amount": trade_event["total_price"],
        "status": "SUCCESS",
        "correlation_id": trade_event["correlation_id"]
    }
