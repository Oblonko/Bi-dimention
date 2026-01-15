from eth_account import Account
import secrets

class WalletManager:
    def create_wallet(self):
        acct = Account.create(secrets.token_hex(32))
        return {
            "address": acct.address,
            "private_key": acct.key.hex()
        }
