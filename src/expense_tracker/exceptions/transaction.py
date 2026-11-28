from decimal import Decimal


class NegativeTransactionException(Exception):
    def __init__(self, amount: Decimal):
        self.amount = amount
        super().__init__(f"Transaction amount must be positive, got {amount}")

class TransactionNotFoundException(Exception):
    def __init__(self, transaction_id: int):
        self.transaction_id = transaction_id
        super().__init__(f"Transaction with id {transaction_id} does not exist")

class InvalidDateRangeException(Exception):
    def __init__(self):
        super().__init__("start_date must be on or before end_date")
