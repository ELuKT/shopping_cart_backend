from pydantic import BaseModel, EmailStr


class UserReq(BaseModel):
    email: EmailStr
    password: str
