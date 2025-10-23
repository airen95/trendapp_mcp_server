class BaseGenerative():
    name: str

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    async def generate_response(self, user_message: str):
        raise 