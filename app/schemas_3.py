from pydantic import BaseModel

# ============================
# Schema for User Signup
# ============================
class UserSignup(BaseModel):
    username: str   # Username for the new user
    password: str   # Plain text password (will be hashed before saving)
    role: str       # Role of the user (e.g., Teacher, Student)


# ============================
# Schema for User Login
# ============================
class Userlogin(BaseModel):
    username: str   # Username entered during login
    password: str   # Password entered during login


# ============================
# Schema for User Output (Response Model)
# ============================
class UserOut(BaseModel):
    id: int         # Unique ID of the user
    username: str   # Username of the user
    role: str       # Role assigned to the user (Teacher / Student)

    class Config:
        from_attributes = True  # Allows ORM objects to be converted to this schema
