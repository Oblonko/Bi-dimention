@dataclass
class Order:
    order_id: str
    pair: str
    side: str           # buy | sell
    type: str           # market | limit
    price: float | None
    qty: float

@dataclass
class Fill:
    order_id: str
    price: float
    qty: float
    fee: float
    fee_currency: str
    ts: pd.Timestamp
