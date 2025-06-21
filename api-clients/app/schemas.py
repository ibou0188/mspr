from pydantic import BaseModel, EmailStr

class ClientBase(BaseModel):
    username: str
    firstName: str
    lastName: str
    name: str
    createdAt: str
    postalCode: str
    city: str
    profileFirstName: str
    profileLastName: str
    companyName: str
    email: EmailStr

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int
    class Config:
        from_attributes = True  # Pydantic v2
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
