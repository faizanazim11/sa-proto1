from fastapi import APIRouter, Request, Response

from scripts.config import Services
from scripts.core.schemas import LoginModel
from scripts.security import SecurityManager, UserDetails

auth_services = APIRouter()


@auth_services.post("/login")
def login_user(login_model: LoginModel, response: Response, request: Request):
    jwt_token = SecurityManager.login(login_model.username, login_model.password)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {jwt_token}",
        httponly=True,
        secure=Services.ENABLE_SSL,
        samesite="strict",
        domain=request.client.host,
        path="/",
    )
    response.headers["Authorization"] = f"Bearer {jwt_token}"
    response.headers["Access-Control-Allow-Origin"] = request.client.host
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Expose-Headers"] = "Authorization"
    response.headers["Access-Control-Max-Age"] = "3600"
    return {"message": "Login successful"}


@auth_services.get("/user")
def get_user(user_details: UserDetails):
    return {"name": user_details.name}
