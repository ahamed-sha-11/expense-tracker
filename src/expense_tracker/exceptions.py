from decimal import Decimal


class CategoryNotFoundException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Category with id {category_id} does not exist")


class CategoryInUseException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Category {category_id} is used by existing transactions")


class NegativeTransactionException(Exception):
    def __init__(self, amount: Decimal):
        self.amount = amount
        super().__init__(f"Transaction amount must be positive, got {amount}")

class TransactionNotFoundException(Exception):
    def __init__(self, transaction_id: int):
        self.transaction_id = transaction_id
        super().__init__(f"Transaction with id {transaction_id} does not exist")
