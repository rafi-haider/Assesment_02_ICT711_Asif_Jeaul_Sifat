def match_trade(seller_event, buyer_event):
    """
    Matches a seller of solar energy with the neighbourhood buyer.

    The minimum of available energy from the seller and the traded energy.
    and buyer demand.
    """

    if seller_event["user_type"] != "seller":
        raise ValueError("First event must be owned by a seller")

    if buyer_event["user_type"] != "buyer":
        raise ValueError("Second event must be owned to a buyer")

    traded_energy = min(
        seller_event["energy_kwh"],
        buyer_event["energy_kwh"]
    )

    price_per_kwh = 0.25
    total_price = round(traded_energy * price_per_kwh, 2)

    return {
        "event_type": "TradeMatchedEvent",
        "seller_id": seller_event["user_id"],
        "buyer_id": buyer_event["user_id"],
        "energy_kwh": traded_energy,
        "price_per_kwh": price_per_kwh,
        "total_price": total_price,
        "correlation_id": seller_event["correlation_id"]
    }
