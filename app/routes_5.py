from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
import database_1, models_2, auth_4, schemas_3

router = APIRouter()

@router.get("/")
def home():
    return {"msg": "Welcome to FastAPI JWT Demo"}


# Signup
@router.post("/signup")
def signup(user: schemas_3.UserSignup, db: Session = Depends(database_1.get_db)):
    existing = db.query(models_2.User).filter(models_2.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exist")
    hashed_pw = auth_4.hash_password(user.password)
    new_user = models_2.User(
        username = user.username,
        password_hash = hashed_pw, 
        role = user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"User create successfully!"}

# Login
@router.post("/login")
def login(user: schemas_3.Userlogin, db: Session = Depends(database_1.get_db)):
    db_user = db.query(models_2.User).filter(models_2.User.username == user.username).first()
    if not db_user or not auth_4.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    token = auth_4.create_jwt(db_user.username, db_user.role)
    return {"access_token": token, "token_type": "bearer"}

# Teacher-only route
@router.get("/teacher-only")
def teacher(request: Request):
    user = request.state.user
    if user["role"] != "Teacher":
        raise HTTPException(status_code=403, detail="Teachers only")
    return {"msg": f"Welcome Teacher {user['sub']}"}

# Student-only route
@router.get("/student-only")
def student(request: Request):
    user = request.state.user
    if user["role"] != "Student":
        raise HTTPException(status_code=403, detail="Students only")
    return {"msg":f"Welcom Student {user['sub']}"}