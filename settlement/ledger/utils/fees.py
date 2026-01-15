def fee_to_usdt(fee, fee_ccy, price):
    if fee_ccy == "USDT":
        return fee
    return fee * price
