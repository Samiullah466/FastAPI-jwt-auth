from pydantic import BaseModel

class UserSignup(BaseModel):
    username : str
    password : str
    role : str
    

class Userlogin(BaseModel):
    username : str
    password : str
    
class UserOut(BaseModel):
    id: int
    username : str
    role : str
    
    class Config:
        from_attributes = True