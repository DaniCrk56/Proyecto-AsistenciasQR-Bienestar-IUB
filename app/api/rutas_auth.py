
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.repositories.usuario_repo import UsuarioRepository


SECRET_KEY = "1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/auth", tags=["Autenticación y JWT"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class DatosLogin(BaseModel):
    correo_institucional: str
    password: str


class DatosRegistro(BaseModel):
    nombres: str
    apellidos: str
    id_tipo_documento: int
    numero_documento: str
    correo_institucional: str
    password: str
    id_programa: int


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/registro")
def registrar_estudiante(datos: DatosRegistro):

    repo = UsuarioRepository()

    if not datos.nombres.strip() or not datos.apellidos.strip():
        raise HTTPException(status_code=400, detail="Completa nombres y apellidos")

    if not datos.numero_documento.strip() or not datos.correo_institucional.strip():
        raise HTTPException(status_code=400, detail="Completa los datos del documento y correo")

    if len(datos.password) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener mínimo 8 caracteres")

    if datos.id_tipo_documento not in [1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="Tipo de documento inválido")

    programas = repo.obtener_programas()

    programa_valido = any(
        programa["id"] == datos.id_programa
        for programa in programas
    )

    if not programa_valido:
        raise HTTPException(status_code=400, detail="Programa académico inválido")

    existentes = repo.verificar_datos_registro(
        datos.correo_institucional.strip(),
        datos.numero_documento.strip()
    )

    if existentes is None:
        raise HTTPException(status_code=500, detail="No fue posible conectar con la base de datos")

    if existentes["correo_existe"]:
        raise HTTPException(status_code=400, detail="Este correo ya está registrado")

    if existentes["documento_existe"]:
        raise HTTPException(status_code=400, detail="Este documento ya está registrado")

    nuevo_id = repo.crear(
        datos.nombres.strip(),
        datos.apellidos.strip(),
        datos.id_tipo_documento,
        datos.numero_documento.strip(),
        datos.correo_institucional.strip(),
        datos.password,
        datos.id_programa,
        3
    )

    if not nuevo_id:
        raise HTTPException(status_code=500, detail="No fue posible registrar el estudiante")

    return {
        "mensaje": "Estudiante registrado exitosamente",
        "id": nuevo_id
    }


@router.post("/login")
def login(datos: DatosLogin):

    repo = UsuarioRepository()
    usuario = repo.obtener_por_correo(datos.correo_institucional)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    password_guardado = usuario.get("password_hash")

    if not password_guardado or datos.password != password_guardado:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

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
            "numero_documento": usuario["numero_documento"],
            "tipo_documento": usuario["tipo_documento"],
            "correo_institucional": usuario["correo_institucional"],
            "programa": usuario["programa"],
            "id_rol": usuario["id_rol"]
        }
    }


@router.post("/token")
def login_swagger(datos: OAuth2PasswordRequestForm = Depends()):

    repo = UsuarioRepository()
    usuario = repo.obtener_por_correo(datos.username)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    password_guardado = usuario.get("password_hash")

    if not password_guardado or datos.password != password_guardado:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

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
        "token_type": "bearer"
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

def validar_administrador(token: str = Depends(oauth2_scheme)):

    exception_auth = HTTPException(
        status_code=401,
        detail="Token inválido o expirado"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        usuario_id = payload.get("usuario_id")
        id_rol = payload.get("id_rol")

        if usuario_id is None or id_rol is None:
            raise exception_auth

        if int(id_rol) != 1:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos de administrador"
            )

        return {
            "usuario_id": int(usuario_id),
            "id_rol": int(id_rol)
        }

    except JWTError:
        raise exception_auth

@router.get("/perfil")
def ver_perfil_protegido(usuario_actual: str = Depends(validar_token)):
    return {
        "mensaje": "Acceso concedido exitosamente con JWT",
        "usuario_autenticado": usuario_actual
    }
