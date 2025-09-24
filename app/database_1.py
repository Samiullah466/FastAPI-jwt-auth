from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------------------------------------------------------
# Database Configuration
# ------------------------------------------------------------------------------

# Connection string for PostgreSQL database
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/mydb"

# Engine: Core interface to the database
engine = create_engine(DATABASE_URL)

# Session factory:
#   - autocommit=False → Explicit commit required
#   - autoflush=False  → Prevents auto-flushing for better control
#   - bind=engine      → Binds the session to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


# ------------------------------------------------------------------------------
# Database Session Dependency
# ------------------------------------------------------------------------------

def get_db():
    """
    Provides a new database session for each request.
    Ensures the session is closed after the request is handled.
    
    Yields:
        Session: SQLAlchemy session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
