from pydantic import BaseModel, EmailStr

#SIGNUP SCHEMA-
class UserCreate(BaseModel):
    email: EmailStr
    password: str


#LOGIN SCHEMA
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

class Config:
        from_attributes = True    