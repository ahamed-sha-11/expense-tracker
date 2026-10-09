from decimal import Decimal


class NegativeTransactionException(Exception):
    def __init__(self, amount: Decimal):
        self.amount = amount
        super().__init__(f"Transaction amount must be positive, got {amount}")


class CategoryNotFoundException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Category with id {category_id} does not exist")
