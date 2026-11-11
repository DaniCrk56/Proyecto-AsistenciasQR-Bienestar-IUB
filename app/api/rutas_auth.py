
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.repositories.usuario_repo import UsuarioRepository

SECRET_KEY = "1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/auth", tags=["Autenticación y JWT"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class DatosLogin(BaseModel):
    correo_institucional: str
    password: str


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(datos: DatosLogin):
    repo = UsuarioRepository()

    usuario = repo.obtener_por_correo(datos.correo_institucional)

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    password_guardado = usuario.get("password_hash")

    if datos.password != password_guardado:
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )

    token = crear_token_acceso(
        data={
            "sub": usuario["correo_institucional"],
            "usuario_id": usuario["id"],
            "id_rol": usuario["id_rol"]
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario["id"],
            "nombres": usuario["nombres"],
            "apellidos": usuario["apellidos"],
            "correo_institucional": usuario["correo_institucional"],
            "id_rol": usuario["id_rol"]
        }
    }


def validar_token(token: str = Depends(oauth2_scheme)):
    exception_auth = HTTPException(
        status_code=401,
        detail="Token inválido o expirado"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

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
