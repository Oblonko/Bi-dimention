class A3Engine:
    def run_window(self, uid, market_df):
        if vault.balance < MIN_SPOT:
            return

        entry_usdt = vault.balance * ENTRY_PCT
        self.entry(uid, entry_usdt)

        fills, glyphs = self.tp_engine.compute(...)
        self.settle(uid, fills, glyphs)
