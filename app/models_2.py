from sqlalchemy import Integer, Column, String
from database_1 import Base

# ------------------------------------------------------------------------------
# User Model
# ------------------------------------------------------------------------------

class User(Base):
    """
    SQLAlchemy ORM model representing the 'Users' table.

    Attributes:
        id (int): Primary key, unique identifier for each user.
        username (str): Unique username, indexed for faster lookup.
        password_hash (str): Hashed password for authentication.
        role (str): User role, e.g., 'Teacher' or 'Student'.
    """
    
    __tablename__ = "Users"   # Database table name
    
    # Columns definition
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "Teacher" / "Student"
