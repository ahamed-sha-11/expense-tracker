class LLMCredentialsAlreadyExistsException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__("LLM credentials are already saved for this user, multi model architecture will be supported in the future")


class LLMCredentialsNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__("No LLM credentials are saved for this user")
