@dataclass
class LedgerRow:
    time: pd.Timestamp
    uid: str
    trade_id: int | None
    glyph: str | None
    action: str
    amount: float
    balance_after: float
