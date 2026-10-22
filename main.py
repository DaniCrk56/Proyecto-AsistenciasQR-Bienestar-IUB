from fastapi import FastAPI
from app.api import (
    rutas_roles,
    rutas_usuarios,
    rutas_modulos,
    rutas_modulo_rol,
    rutas_tipo_documento,
    rutas_programas,
    rutas_lugares,
    rutas_categoria_Actividad,
    rutas_estado_actividad,
    rutas_actividades,
    ruta_inscripcion,
    ruta_asistencia,
    rutas_auth
)

app = FastAPI(
    title="API de Bienestar Universitario",
    description="Sistema modular de gestión y asistencia con FastAPI y PostgreSQL",
    version="1.0.0"
)

app.include_router(rutas_roles.router)
app.include_router(rutas_usuarios.router)
app.include_router(rutas_modulos.router)
app.include_router(rutas_modulo_rol.router)
app.include_router(rutas_tipo_documento.router)
app.include_router(rutas_programas.router)
app.include_router(rutas_lugares.router)
app.include_router(rutas_categoria_Actividad.router)
app.include_router(rutas_estado_actividad.router)
app.include_router(rutas_actividades.router)
app.include_router(ruta_inscripcion.router)
app.include_router(ruta_asistencia.router)
app.include_router(rutas_auth.router)

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API de Bienestar Universitario - FastAPI funcionando al 100%"}
