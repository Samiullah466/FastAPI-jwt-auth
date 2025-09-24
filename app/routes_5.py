from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import database_1, models_2, auth_4, schemas_3
import pandas as pd
import io, uuid, os

router = APIRouter()


@router.get("/")
def home():
    # Root endpoint - just a welcome message
    return {"msg": "Welcome to FastAPI JWT Demo"}


# ============================
# Signup Endpoint
# ============================
@router.post("/signup")
def signup(user: schemas_3.UserSignup, db: Session = Depends(database_1.get_db)):
    # Check if username already exists
    existing = db.query(models_2.User).filter(models_2.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exist")
    
    # Hash the password before storing
    hashed_pw = auth_4.hash_password(user.password)
    
    # Create new user object
    new_user = models_2.User(
        username=user.username,
        password_hash=hashed_pw, 
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"User create successfully!"}


# ============================
# Login Endpoint
# ============================
@router.post("/login")
def login(user: schemas_3.Userlogin, db: Session = Depends(database_1.get_db)):
    # Check if user exists in DB
    db_user = db.query(models_2.User).filter(models_2.User.username == user.username).first()
    
    # If not found or password mismatch → Invalid credentials
    if not db_user or not auth_4.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    # Generate JWT token
    token = auth_4.create_jwt(db_user.username, db_user.role)
    return {"access_token": token, "token_type": "bearer"}


# ============================
# Teacher-only Route
# ============================
@router.get("/teacher-only")
def teacher(request: Request):
    # Extract user from JWT (via middleware)
    user = request.state.user
    
    # Allow only Teachers
    if user["role"] != "Teacher":
        raise HTTPException(status_code=403, detail="Teachers only")
    
    return {"msg": f"Welcome Teacher {user['sub']}"}


# ============================
# Student-only Route
# ============================
@router.get("/student-only")
def student(request: Request):
    # Extract user from JWT
    user = request.state.user
    
    # Allow only Students
    if user["role"] != "Student":
        raise HTTPException(status_code=403, detail="Students only")
    
    return {"msg":f"Welcom Student {user['sub']}"}


# ============================
# Delete user by ID (Teacher only)
# ============================
@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, request: Request, db: Session = Depends(database_1.get_db)):
    # Get logged-in user from JWT
    user = request.state.user  

    # Only Teacher is allowed to delete users
    if user["role"] != "Teacher":
        raise HTTPException(status_code=403, detail="Only Teacher can delete users")

    # Find user by ID
    db_user = db.query(models_2.User).filter(models_2.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")

    # Delete user and commit changes
    db.delete(db_user)
    db.commit()
    return {"msg": f"User with id={user_id} deleted successfully"}


# ============================
# Excel Upload Endpoint (Teacher only)
# ============================
@router.post("/upload-excel")
async def upload_excel(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(database_1.get_db)
):
    # Verify that only Teachers can upload Excel
    user = request.state.user
    if user["role"] != "Teacher":
        raise HTTPException(status_code=403, detail="Only Teacher can upload Excel")

    # Check if uploaded file is .xlsx
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")

    # Read Excel file into Pandas DataFrame
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    # Ensure required columns are present
    required_columns = {"username", "password_hash", "role"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"Excel must contain {required_columns}")

    added, skipped = 0, 0
    duplicates = []

    # Iterate through rows and insert into DB
    for _, row in df.iterrows():
        existing = db.query(models_2.User).filter(models_2.User.username == row["username"]).first()
        if existing:
            skipped += 1
            duplicates.append(row["username"])
            continue

        # Hash password before saving
        hashed_pw = auth_4.hash_password(str(row["password_hash"]))
        new_user = models_2.User(
            username=row["username"],
            password_hash=hashed_pw,
            role=row["role"]
        )
        db.add(new_user)
        added += 1

    db.commit()

    return {
        "total_rows": len(df),
        "added_users": added,
        "skipped_users": skipped,
        "duplicates": duplicates
    }


# ============================
# Download Users as Excel (Teacher only)
# ============================
@router.get("/download-excel")
def download_excel(request: Request, db: Session = Depends(database_1.get_db)):
    # Only Teacher is allowed to download Excel
    user = request.state.user
    if user["role"] != "Teacher":
        raise HTTPException(status_code=403, detail="Only Teacher can download Excel")

    # Fetch all users from DB
    users = db.query(models_2.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found in DB")

    # Convert users into DataFrame
    data = [{"id": u.id, "username": u.username, "role": u.role} for u in users]
    df = pd.DataFrame(data)

    # Save DataFrame as Excel file
    filename = f"users_{uuid.uuid4().hex}.xlsx"
    filepath = os.path.join(os.getcwd(), filename)
    df.to_excel(filepath, index=False)

    # Return Excel file as response
    return FileResponse(
        filepath,
        filename="users.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
