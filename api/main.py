app = FastAPI()
app.include_router(trade_router)
app.include_router(withdraw_router)
