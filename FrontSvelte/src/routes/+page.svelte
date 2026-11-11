
<script>
    import { iniciarSesion } from '#lib/services/api_autht.js';

    let correo_institucional = '';
    let password = '';
    let mensaje = '';
    let error = false;

   async function manejarSubmit(evento) {
    evento.preventDefault();

    mensaje = '';
    error = false;

    try {
        const respuesta = await iniciarSesion(
            correo_institucional,
            password
        );

        localStorage.setItem('token', respuesta.access_token);
        localStorage.setItem('usuario', JSON.stringify(respuesta.usuario));

        mensaje = '¡Inicio de sesión exitoso!';

        if (respuesta.usuario.id_rol === 1) {
            window.location.href = '/admin/admin';
        } 
        else if (respuesta.usuario.id_rol === 3) {
            window.location.href = '/estudiantes/eventos';
        } 
        else {
            error = true;
            mensaje = 'Tu cuenta no tiene un rol autorizado para ingresar.';
        }

    } catch (e) {
        error = true;
        mensaje = e.message;
    }
}
</script>

<div class="login-card">
    <div class="logo-area">
        <img src="/LogoIUB.png" alt="Institución Universitaria de Barranquilla" class="logo-auth" />
        <div class="fallback-title">INSTITUCIÓN UNIVERSITARIA DE BARRANQUILLA</div>
    </div>

    <p class="instruction-text">
        Identifíquese usando su cuenta institucional:
    </p>

    {#if mensaje}
        <div class:error-msg={error} class:success-msg={!error}>
            {mensaje}
        </div>
    {/if}

    <form onsubmit={manejarSubmit}>
        <div class="form-group">
            <label for="correo">Correo Institucional</label>
            <input
                type="email"
                id="correo"
                bind:value={correo_institucional}
                placeholder="tucorreo@iub.edu.co"
                required
            />
        </div>

        <div class="form-group">
            <label for="password">Contraseña</label>
            <input
                type="password"
                id="password"
                bind:value={password}
                placeholder="••••••••"
                required
            />
        </div>

        <button type="submit" class="btn-submit">
            Acceder
        </button>
    </form>
</div>

<style>
    .login-card {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        padding: 2.5rem;
        width: 100%;
        max-width: 440px;
        box-sizing: border-box;
        margin: auto;
    }

    .logo-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .logo-auth {
        max-height: 60px;
        width: auto;
        object-fit: contain;
        margin-bottom: 0.5rem;
    }

    .fallback-title {
        font-weight: 800;
        color: #121420;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }

    .instruction-text {
        font-size: 1rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 0.75rem;
    }

    .error-msg {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 0.75rem;
        border-radius: 8px;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    .success-msg {
        background-color: #dcfce7;
        color: #166534;
        padding: 0.75rem;
        border-radius: 8px;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    .form-group {
        margin-bottom: 1.25rem;
    }

    label {
        display: block;
        margin-bottom: 0.4rem;
        font-weight: 600;
        color: #4b5563;
        font-size: 0.9rem;
    }

    input {
        width: 100%;
        padding: 0.8rem 1rem;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-size: 1rem;
        box-sizing: border-box;
        background-color: #f8fafc;
        transition: all 0.2s;
    }

    input:focus {
        outline: none;
        border-color: #121420;
        background-color: #fff;
        box-shadow: 0 0 0 3px rgba(18, 20, 32, 0.1);
    }

    .btn-submit {
        width: 100%;
        background-color: #121420;
        color: white;
        padding: 0.85rem;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.2s;
        margin-top: 0.5rem;
    }

    .btn-submit:hover {
        background-color: #1e293b;
    }
</style>
