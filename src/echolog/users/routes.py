from fastapi import APIRouter

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/")
def get_users():
    return {"message": "Hello Users"}
