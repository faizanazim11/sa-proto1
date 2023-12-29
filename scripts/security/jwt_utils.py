import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, MissingRequiredClaimError

from scripts.config.logging import logger


class JWT:
    """
    Class for creating and verifying JWT tokens using HS256 algorithm,
    using the secret key provided in the config file.
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """
        Initialize the JWT object.

        Args:
            secret_key (str): The secret key used for encoding and decoding the JWT.
            algorithm (str, optional): The algorithm used for encoding and decoding the JWT. Defaults to "HS256".
        """
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode(self, payload: dict) -> str:
        """
        Encode the payload into a JWT token.

        Args:
            payload (dict): The payload to be encoded.

        Returns:
            str: The encoded JWT token.
        """
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> dict:
        """
        Decode the JWT token and retrieve the payload.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            dict: The decoded payload.
        """
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def verify(self, token: str) -> bool:
        """
        Verify the validity of the JWT token.

        Args:
            token (str): The JWT token to be verified.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            self.decode(token)
            return True
        except (ExpiredSignatureError, InvalidSignatureError, MissingRequiredClaimError) as e:
            logger.error("Failed to verify token: %s", e)
            return False

    def get_payload(self, token: str) -> dict:
        """
        Get the payload from the JWT token.

        Args:
            token (str): The JWT token.

        Returns:
            dict: The payload from the JWT token.
        """
        try:
            return self.decode(token)
        except (ExpiredSignatureError, InvalidSignatureError, MissingRequiredClaimError) as e:
            logger.error("Failed to verify token: %s", e)
            return {}

    def get_username(self, token: str) -> str:
        """
        Get the user ID from the JWT token.

        Args:
            token (str): The JWT token.

        Returns:
            str: The user ID from the JWT token.
        """
        payload = self.get_payload(token)
        return payload.get("username", "")
