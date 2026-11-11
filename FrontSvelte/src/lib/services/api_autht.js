
const URL_BASE = 'https://proyecto-asistenciasqr-bienestar-iub.onrender.com/auth';

async function procesarRespuesta(respuesta) {
    if (!respuesta.ok) {
        const errorData = await respuesta.json().catch(() => ({}));
        throw new Error(
            errorData.detail || 'Error ' + respuesta.status
        );
    }

    return await respuesta.json();
}

export async function iniciarSesion(correo_institucional, password) {
    const respuesta = await fetch(`${URL_BASE}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            correo_institucional,
            password
        })
    });

    return await procesarRespuesta(respuesta);
}

export async function registrarEstudiante(datos) {
    const respuesta = await fetch(`${URL_BASE}/registro`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    });

    return await procesarRespuesta(respuesta);
}
