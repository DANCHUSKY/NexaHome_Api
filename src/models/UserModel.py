from pydantic import BaseModel

class UserLoged(BaseModel):
    email: str
    passw:str

class UserRegisted(BaseModel):
    name: str
    email: str
    passw: str
    phone: str   