@dataclass(frozen=True)
class User:
    uid: str
    email: str
    whitelisted: bool
    eth_address: str
