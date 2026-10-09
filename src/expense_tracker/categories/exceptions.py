class CategoryNotFoundException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Category with id {category_id} does not exist")
