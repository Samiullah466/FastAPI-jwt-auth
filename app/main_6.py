from fastapi import FastAPI, Request, HTTPException
import auth_4, routes_5
from fastapi.responses import JSONResponse

app = FastAPI()

# Register all routes from routes_5.py
app.include_router(routes_5.router)

# ----------------- MIDDLEWARE -----------------
@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    # Skip JWT validation for public routes
    if request.url.path in ["/login", "/signup", "/docs", "/openapi.json","/"]:
        return await call_next(request)

    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT and attach user info to request state
        user_data = auth_4.decode_jwt(token)
        request.state.user = user_data

        # Print user data in VS Code terminal
        print("\n JWT Decoded Payload:")
        print(user_data)
        print("Requested Path:", request.url.path)
        print("-----------------------------\n")

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Unexpected error: {str(e)}"})

    return await call_next(request)
