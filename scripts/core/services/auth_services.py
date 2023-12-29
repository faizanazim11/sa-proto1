from fastapi import APIRouter, Response

from scripts.core.schemas import LoginModel
from scripts.security import SecurityManager, UserDetails

auth_services = APIRouter()


@auth_services.post("/login")
def login_user(login_model: LoginModel, response: Response):
    jwt_token = SecurityManager.login(login_model.username, login_model.password)
    response.set_cookie(key="Authentication", value=f"Bearer {jwt_token}", httponly=True)
    response.headers["Authorization"] = f"Bearer {jwt_token}"
    return {"message": "Login successful"}


@auth_services.get("/user")
def get_user(user_details: UserDetails):
    return f"Hello {user_details.name}"
