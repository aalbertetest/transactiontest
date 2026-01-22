import uuid


class RetryableProcessorError(Exception):
    pass


class ProcessorDeclinedError(Exception):
    pass


class ProcessorClient:
    def authorize(self, amount: int, currency: str, payment_method_token: str) -> str:
        if amount % 13 == 0:
            raise RetryableProcessorError("temporary processor timeout")
        if amount % 7 == 0:
            raise ProcessorDeclinedError("card declined")
        return f"proc_{uuid.uuid4().hex[:20]}"
