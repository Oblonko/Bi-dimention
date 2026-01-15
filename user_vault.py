@dataclass
class Vault:
    uid: str
    balance: float
    locked: float   # active window capital
