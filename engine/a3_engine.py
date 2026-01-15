class A3Engine:
    def run_window(self, user, df):
        if user.vault.balance < MIN_SPOT:
            return

        entry = user.vault.balance * ENTRY_PCT
        user.vault.lock(entry)

        fills, glyphs = self.tp.compute(...)
        self.settle(user, fills, glyphs)
