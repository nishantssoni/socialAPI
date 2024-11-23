# jwt authenticccation
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status, Depends
import schemas
from jwt import PyJWTError 
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# secret key
SECRET_KEY = "4cce9f493ea02288538acd87b3a1f3522137c1a1db868955849df9070b6b26e4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# verify access token
def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # converted to string because id is int and schema expects string
        token_data = schemas.TokenData(id=str(id))
    except PyJWTError:
        raise credentials_exception

    return token_data

# get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)