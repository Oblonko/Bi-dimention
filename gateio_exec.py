import time
import hmac
import hashlib
import requests
import pandas as pd
from typing import List
from .models import Order, Fill

BASE_URL = "https://api.gateio.ws/api/v4"

class GateIOExec:

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret.encode()

    # -------------------------
    # AUTH
    # -------------------------
    def _sign(self, method, path, body=""):
        ts = str(int(time.time()))
        msg = f"{method}\n{path}\n{body}\n{ts}"
        sig = hmac.new(self.secret, msg.encode(), hashlib.sha512).hexdigest()
        return {
            "KEY": self.key,
            "SIGN": sig,
            "Timestamp": ts
        }

    # -------------------------
    # MARKET BUY (ENTRY)
    # -------------------------
    def market_buy(self, pair: str, usdt: float) -> Order:
        body = {
            "currency_pair": pair,
            "side": "buy",
            "type": "market",
            "amount": str(usdt)
        }
        path = "/spot/orders"
        headers = self._sign("POST", path, str(body))
        r = requests.post(BASE_URL + path, json=body, headers=headers)
        r.raise_for_status()
        o = r.json()

        return Order(
            order_id=o["id"],
            pair=pair,
            side="buy",
            type="market",
            price=None,
            qty=float(o["filled_amount"])
        )

    # -------------------------
    # LIMIT SELL (TP)
    # -------------------------
    def limit_sell(self, pair: str, qty: float, price: float) -> Order:
        body = {
            "currency_pair": pair,
            "side": "sell",
            "type": "limit",
            "price": f"{price:.6f}",
            "amount": f"{qty:.6f}"
        }
        path = "/spot/orders"
        headers = self._sign("POST", path, str(body))
        r = requests.post(BASE_URL + path, json=body, headers=headers)
        r.raise_for_status()
        o = r.json()

        return Order(
            order_id=o["id"],
            pair=pair,
            side="sell",
            type="limit",
            price=price,
            qty=qty
        )

    # -------------------------
    # FETCH FILLS (DETERMINISTIC)
    # -------------------------
    def fetch_fills(self, order_id: str) -> List[Fill]:
        path = f"/spot/trades?order_id={order_id}"
        headers = self._sign("GET", path)
        r = requests.get(BASE_URL + path, headers=headers)
        r.raise_for_status()

        fills = []
        for f in r.json():
            fills.append(
                Fill(
                    order_id=order_id,
                    price=float(f["price"]),
                    qty=float(f["amount"]),
                    fee=float(f["fee"]),
                    fee_currency=f["fee_currency"],
                    ts=pd.to_datetime(f["create_time"], unit="s")
                )
            )
        return fills
