@router.post("/trade/run")
def run_trade(user=Depends(auth)):
    engine.run_window(...)
