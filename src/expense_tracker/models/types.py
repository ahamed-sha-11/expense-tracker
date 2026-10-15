import enum

from sqlalchemy import Integer, TypeDecorator


class TransactionType(enum.IntEnum):
    INCOME = 1
    EXPENSE = 2


class IntEnumType(TypeDecorator):
    impl = Integer
    cache_ok = True

    def __init__(self, enum_type):
        super().__init__()
        self.enum_type = enum_type

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return int(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_type(value)
