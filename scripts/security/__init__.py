from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel
from typing_extensions import Annotated

from scripts.config import SecurityConstants
from scripts.core.db.mongo.collections.users import UsersCollection
from scripts.security.jwt_utils import JWT


class _UserDetails(BaseModel):
    username: str
    name: str


class _SecurityManager:
    def __init__(self):
        self.jwt = JWT(SecurityConstants.TOKEN)

    def login(self, username: str, password: str) -> str:
        """
        Login the user and return the JWT token.
        :param username:
        :param password:
        :return:
        """
        user = UsersCollection().get_user(username)
        if user and user["password"] == password:
            return self.jwt.encode({"username": username, "name": user["name"]})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def __call__(self, request: Request) -> _UserDetails:
        """
        Verify the validity of the JWT token.
        :param token:
        :return:
        """
        try:
            token = request.headers.get("proto-token", request.cookies.get("Authentication", ""))
            token = token.split(" ")[1]
            if self.jwt.verify(token):
                return _UserDetails(**self.jwt.get_payload(token))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )


SecurityManager = _SecurityManager()
UserDetails = Annotated[_UserDetails, Depends(SecurityManager)]

__all__ = ["UserDetails", "SecurityManager"]
