from pydantic import BaseModel, EmailStr


class ResendEmailReq(BaseModel):
    email: EmailStr