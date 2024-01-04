from fastapi import APIRouter, Response

from scripts.core.schemas import LoginModel
from scripts.security import SecurityManager, UserDetails

auth_services = APIRouter()


@auth_services.post("/login")
def login_user(login_model: LoginModel, response: Response):
    jwt_token = SecurityManager.login(login_model.username, login_model.password)
    response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True, secure=False, samesite='strict', domain='be.faizanazim11.codes', path='/')
    response.headers["access_token"] = f"Bearer {jwt_token}"
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Expose-Headers"] = "access_token"
    response.headers["Access-Control-Max-Age"] = "3600"
    return {"message": "Login successful"}


@auth_services.get("/user")
def get_user(user_details: UserDetails):
    return user_details.name
