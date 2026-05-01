from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class TransactionCreate(BaseModel):
    sender: str
    receiver: str
    amount: float

class Token(BaseModel):
    access_token: str
    token_type: str
