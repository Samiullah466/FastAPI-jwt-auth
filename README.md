# FastAPI + PostgreSQL + Alembic + JWT Authentication

This project is a **FastAPI-based authentication and authorization system** with role-based access control.  
It supports **signup, login, JWT authentication, middleware-based request validation, and role-based authorization (Teacher & Student).**



## Features
- User **Signup & Login** with password hashing (bcrypt).
- Secure authentication using **JWT (JSON Web Token)**.
- **Role-based access control** (Teacher & Student).
- **Middleware** for token validation and request authentication.
- PostgreSQL database integration using **SQLAlchemy ORM**.
- **Alembic migrations** for database schema management.



## Tech Stack
- **FastAPI** (Web Framework)
- **PostgreSQL** (Database)
- **SQLAlchemy** (ORM)
- **Alembic** (Database migrations)
- **bcrypt** (Password hashing)
- **JWT (PyJWT)** (Authentication)



##  Setup Instructions

### Clone Repository
```bash
git clone https://github.com/your-username/fastapi-auth-system.git
cd fastapi-auth-system
