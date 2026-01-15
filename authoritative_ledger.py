@dataclass
class LedgerRow:
    time: pd.Timestamp
    uid: str
    trade_id: Optional[int]
    glyph: Optional[str]
    action: str
    amount: float
    balance_after: float
