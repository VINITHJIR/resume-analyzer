from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def create_token(data: dict):
    data_copy = data.copy()
    data_copy["exp"] = datetime.utcnow() + timedelta(hours=2)

    return jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)