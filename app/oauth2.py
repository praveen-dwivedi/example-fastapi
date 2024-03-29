from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_schemes = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Alorithm
#Expiration time

# SECRET_KEY = "5ccea7a8339f1f691caaa5f7a2d7810497a6074f86881313f7404d0d0786e490" #openssl rand -hex 32
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

SECRET_KEY = settings.secret_key #openssl rand -hex 32
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")

        if id is None:
            raise credential_exception
    
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credential_exception
    
    return token_data


def get_current_user(token : str = Depends(oauth2_schemes)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credential_exception)      