import jwt
from dotenv import load_dotenv
import os
import base64


def validate_token(token):
    try:
        load_dotenv()
        signature = base64.b64decode(os.environ["jwt_secret_key"])
        return {
            "code": 200,
            "message": "TOKEN_VALID",
            "data": jwt.decode(token, signature, algorithms="HS256"),
        }

    except jwt.ExpiredSignatureError:
        return {"code": 500, "message": "TOKEN_EXPIRED", "data": ""}

    except jwt.InvalidTokenError:
        return {"code": 500, "message": "TOKEN_INVALID", "data": ""}
