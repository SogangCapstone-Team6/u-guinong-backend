from fastapi import APIRouter

router = APIRouter(
    prefix="/api/auth"
)

@router.post("/signup")
def auth_signup():
    return {"response": "signup"}

@router.post("/login")
def auth_login():
    return {"response": "login"}
