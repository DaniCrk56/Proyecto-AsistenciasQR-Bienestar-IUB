
const URL_BASE = 'https://proyecto-asistenciasqr-bienestar-iub.onrender.com/auth/login';
async function procesarRespuesta(respuesta) {
    if (!respuesta.ok) {
        const errorData = await respuesta.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Error ' + respuesta.status + ': Credenciales inválidas');
    }
    return await respuesta.json();
}

/**
 * 
 * @param {string} correo_institucional 
 * @param {string} password 
 */
export async function iniciarSesion(correo_institucional, password) {
    const respuesta = await fetch(URL_BASE, {
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
