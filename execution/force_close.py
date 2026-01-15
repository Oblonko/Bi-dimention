def force_close(self, pair, remaining_qty):
    return self.market_sell(pair, remaining_qty)
