from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from app.repositories.usuario_repo import UsuarioRepository

SECRET_KEY = "1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/auth", tags=["Autenticación y JWT"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    repo = UsuarioRepository()
    
    usuarios = repo.obtener_todos()
    usuario_encontrado = None
    
    for u in usuarios:
        if u.get("email") == form_data.username or u.get("username") == form_data.username:
            usuario_encontrado = u
            break
            
    if not usuario_encontrado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas: usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_jwt = crear_token_acceso(
        data={"sub": form_data.username, "usuario_id": usuario_encontrado.get("id")},
        expires_delta=access_token_expires
    )

    return {"access_token": token_jwt, "token_type": "bearer"}

def validar_token(token: str = Depends(oauth2_scheme)):
    exception_auth = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exception_auth
    except JWTError:
        raise exception_auth
    return username

@router.get("/perfil")
def ver_perfil_protegido(usuario_actual: str = Depends(validar_token)):
    return {
        "mensaje": "Acceso concedido exitosamente con JWT",
        "usuario_autenticado": usuario_actual
    }