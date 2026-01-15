@dataclass
class Vault:
    uid: str
    balance: float
    locked: float = 0.0

    def lock(self, amt): self.balance -= amt; self.locked += amt
    def unlock(self, amt): self.locked -= amt; self.balance += amt
