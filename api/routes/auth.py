from fastapi import APIRouter, HTTPException
from api.core.security import create_access_token

router = APIRouter(tags=["Auth"])

USERS = {
    "admin": "admin123"
}


@router.post("/login")
def login(username: str, password: str):

    if USERS.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user": username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
