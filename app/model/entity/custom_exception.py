from beanie import Document, Indexed

class CustomException(Document):
    error_code: Indexed(str, unique=True)
    description: str

    class Settings:
        name = "custom_exception"
