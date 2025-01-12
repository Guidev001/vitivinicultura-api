from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.models.user.user import User
from app.utils.password_utils import verify_password

security = HTTPBasic()


async def authenticate_user(request: Request, db: Session):
    """
    Verifica credenciais básicas enviadas no cabeçalho da requisição.
    """
    try:
        credentials: HTTPBasicCredentials = await security(request)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"}
        )

    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    return user
