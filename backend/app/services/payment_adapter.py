class MockPaymentAdapter:
    async def charge(self, amount: float, vendor: str) -> dict:
        return {"status": "SUCCESS", "provider": "mock", "vendor": vendor, "amount": str(amount)}


payment_adapter = MockPaymentAdapter()
