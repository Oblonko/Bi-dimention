from eth_account import Account
import secrets

def create_eth_wallet():
    acct = Account.create(secrets.token_hex(32))
    return acct.address, acct.key.hex()
