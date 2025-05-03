from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_master(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        master_id: int = payload.get("master_id")
        if master_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return {"master_id": master_id}