import bcrypt, jwt, time
from fastapi import HTTPException
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def verify_password(password:str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

def create_jwt(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": time.time() + 300 # 5 Minutea expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    