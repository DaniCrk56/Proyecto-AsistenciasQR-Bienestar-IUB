
<script>
    import { iniciarSesion } from '#lib/services/api_autht.js';

    let correo_institucional = '';
    let password = '';
    let mensaje = '';
    let error = false;
    let cargando = false;

    async function manejarSubmit(evento) {
        evento.preventDefault();

        mensaje = '';
        error = false;
        cargando = true;

        try {
            const respuesta = await iniciarSesion(
                correo_institucional,
                password
            );

            localStorage.setItem('token', respuesta.access_token);
            localStorage.setItem('usuario', JSON.stringify(respuesta.usuario));

            if (respuesta.usuario.id_rol === 1) {
                mensaje = '¡Bienvenido al sistema!';
                window.location.href = '/admin/admin';
            }
            else if (respuesta.usuario.id_rol === 3) {
                mensaje = '¡Bienvenido al sistema!';
                window.location.href = '/estudiantes/eventos';
            }
            else {
                error = true;
                mensaje = 'Tu cuenta no tiene un rol autorizado para ingresar.';
            }

        } catch (e) {
            error = true;
            mensaje = e.message;
        } finally {
            cargando = false;
        }
    }
</script>

<svelte:head>
    <title>Iniciar sesión | Bienestar Universitario IUB</title>
    <meta name="description" content="Acceso al sistema de gestión de eventos de Bienestar Universitario." />
</svelte:head>

<div class="pagina-login">

    <div class="decoracion decoracion-uno"></div>
    <div class="decoracion decoracion-dos"></div>
    <div class="decoracion decoracion-tres"></div>

    <div class="contenido-login">

        <div class="login-card">

            <div class="franja-superior"></div>

            <div class="logo-area">
                <div class="logo-contenedor">
                    <img
                        src="/LogoIUB.png"
                        alt="Institución Universitaria de Barranquilla"
                        class="logo-auth"
                    />
                </div>

                <div class="fallback-title">
                    INSTITUCIÓN UNIVERSITARIA DE BARRANQUILLA
                </div>

                <div class="separador-logo"></div>

                <span class="etiqueta-sistema">
                    BIENESTAR UNIVERSITARIO
                </span>
            </div>

            <div class="bienvenida">
                <h1>¡Bienvenido!</h1>
                <p>Ingresa a tu cuenta institucional para continuar.</p>
            </div>

            <div class="instruction-text">
                <span class="punto"></span>
                Identifícate con tus credenciales institucionales
            </div>

            {#if mensaje}
                <div class="mensaje" class:error-msg={error} class:success-msg={!error}>
                    <span>{error ? '⚠' : '✓'}</span>
                    {mensaje}
                </div>
            {/if}

            <form onsubmit={manejarSubmit}>

                <div class="form-group">
                    <label for="correo">Correo institucional</label>

                    <div class="input-contenedor">
                        <span class="icono-input">✉</span>
                        <input
                            type="email"
                            id="correo"
                            bind:value={correo_institucional}
                            placeholder="tucorreo@unibarranquilla.edu.co"
                            autocomplete="username"
                            required
                        />
                    </div>
                </div>

                <div class="form-group">
                    <label for="password">Contraseña</label>

                    <div class="input-contenedor">
                        <span class="icono-input">🔒</span>
                        <input
                            type="password"
                            id="password"
                            bind:value={password}
                            placeholder="Ingresa tu contraseña"
                            autocomplete="current-password"
                            required
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    class="btn-submit"
                    disabled={cargando}
                >
                    {#if cargando}
                        <span class="spinner"></span>
                        Verificando...
                    {:else}
                        Iniciar sesión
                        <span class="flecha">→</span>
                    {/if}
                </button>

            </form>

            <div class="registro-enlace">
                <span>¿No tienes una cuenta?</span>
                <a href="/registro">Regístrate aquí</a>
            </div>

            <div class="linea-inferior"></div>

            <div class="linea-inferior"></div>

            <div class="mensaje-seguridad">
                <span>🔐</span>
                Acceso exclusivo para usuarios institucionales
            </div>

        </div>

        <footer class="footer-login">
            <p>Institución Universitaria de Barranquilla</p>
            <span>Sistema de Gestión de Eventos Universitarios</span>
            <span class="copyright">© 2026 - Bienestar Universitario</span>
        </footer>

    </div>
</div>

<style>
    :global(*) {
        box-sizing: border-box;
    }

    :global(body) {
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    .pagina-login {
        min-height: 100vh;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 35px 20px;
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #eaf8ff 0%, #d5efff 45%, #edf8ff 100%);
    }

    .contenido-login {
        width: 100%;
        max-width: 440px;
        position: relative;
        z-index: 2;
        animation: aparecer 0.8s ease;
    }

    .decoracion {
        position: absolute;
        border-radius: 50%;
        pointer-events: none;
    }

    .decoracion-uno {
        width: 420px;
        height: 420px;
        background: rgba(0, 174, 239, 0.10);
        top: -170px;
        left: -130px;
    }

    .decoracion-dos {
        width: 520px;
        height: 520px;
        background: rgba(11, 132, 87, 0.08);
        bottom: -240px;
        right: -180px;
    }

    .decoracion-tres {
        width: 180px;
        height: 180px;
        border: 2px solid rgba(0, 174, 239, 0.15);
        top: 18%;
        right: 12%;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(15, 55, 80, 0.13);
        border: 1px solid rgba(255, 255, 255, 0.9);
        padding: 38px 38px 30px;
        width: 100%;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .login-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 25px 65px rgba(15, 55, 80, 0.17);
    }

    .franja-superior {
        height: 6px;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(90deg, #00aeef, #0b8457);
    }

    .logo-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 28px;
        text-align: center;
    }

    .logo-contenedor {
        width: 110px;
        height: 85px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 12px;
    }

    .logo-auth {
        max-height: 80px;
        max-width: 110px;
        width: auto;
        object-fit: contain;
    }

    .fallback-title {
        font-weight: 800;
        color: #172b3a;
        font-size: 0.78rem;
        letter-spacing: 0.5px;
    }

    .separador-logo {
        width: 45px;
        height: 3px;
        background: linear-gradient(90deg, #00aeef, #0b8457);
        border-radius: 10px;
        margin: 15px 0 12px;
    }

    .etiqueta-sistema {
        color: #008cbd;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 2px;
    }

    .bienvenida {
        text-align: center;
        margin-bottom: 28px;
    }

    .bienvenida h1 {
        color: #172b3a;
        font-size: 2rem;
        margin: 0 0 8px;
        font-weight: 800;
    }

    .bienvenida p {
        color: #718096;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.5;
    }

    .instruction-text {
        display: flex;
        align-items: center;
        gap: 9px;
        font-size: 0.85rem;
        font-weight: 650;
        color: #405366;
        margin-bottom: 22px;
    }

    .punto {
        width: 8px;
        height: 8px;
        background: #00aeef;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .mensaje {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 9px;
        padding: 12px;
        border-radius: 10px;
        font-size: 0.85rem;
        margin-bottom: 18px;
        text-align: center;
        animation: aparecer 0.3s ease;
    }

    .error-msg {
        background: #fff0f0;
        color: #bc3030;
        border: 1px solid #ffd3d3;
    }

    .success-msg {
        background: #e9f9ef;
        color: #187b43;
        border: 1px solid #c7eed5;
    }

    .form-group {
        margin-bottom: 21px;
    }

    label {
        display: block;
        margin-bottom: 9px;
        font-weight: 700;
        color: #34495e;
        font-size: 0.88rem;
    }

    .input-contenedor {
        position: relative;
        display: flex;
        align-items: center;
    }

    .icono-input {
        position: absolute;
        left: 15px;
        font-size: 1rem;
        z-index: 1;
        opacity: 0.65;
    }

    input {
        width: 100%;
        padding: 14px 15px 14px 45px;
        border: 1px solid #dce5ed;
        border-radius: 11px;
        font-size: 0.92rem;
        background: #f8fbfd;
        color: #263746;
        outline: none;
        transition: all 0.25s ease;
    }

    input::placeholder {
        color: #a3b0bc;
    }

    input:focus {
        border-color: #00aeef;
        background: #ffffff;
        box-shadow: 0 0 0 4px rgba(0, 174, 239, 0.11);
    }

    .btn-submit {
        width: 100%;
        min-height: 51px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: linear-gradient(110deg, #00aeef, #087eaa);
        color: white;
        padding: 14px;
        border: none;
        border-radius: 11px;
        font-size: 0.97rem;
        font-weight: 750;
        cursor: pointer;
        margin-top: 10px;
        box-shadow: 0 7px 17px rgba(0, 174, 239, 0.23);
        transition: all 0.25s ease;
    }

    .btn-submit:hover:not(:disabled) {
        background: linear-gradient(110deg, #009bd6, #066d94);
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(0, 174, 239, 0.32);
    }

    .btn-submit:active:not(:disabled) {
        transform: scale(0.98);
    }

    .btn-submit:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .flecha {
        font-size: 1.25rem;
        transition: transform 0.25s ease;
    }

    .btn-submit:hover .flecha {
        transform: translateX(5px);
    }

    .spinner {
        width: 17px;
        height: 17px;
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-top-color: white;
        border-radius: 50%;
        animation: girar 0.7s linear infinite;
    }

    .linea-inferior {
        height: 1px;
        background: #edf1f5;
        margin: 26px 0 18px;
    }

    .mensaje-seguridad {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        color: #82909d;
        font-size: 0.75rem;
        text-align: center;
    }

    .footer-login {
        text-align: center;
        margin-top: 24px;
        color: #567184;
        display: flex;
        flex-direction: column;
        gap: 5px;
        font-size: 0.78rem;
    }

    .footer-login p {
        margin: 0;
        font-weight: 700;
        color: #38566b;
    }

    .copyright {
        margin-top: 5px;
        color: #8299a8;
        font-size: 0.72rem;
    }

    @keyframes aparecer {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes girar {
        to {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 500px) {
        .pagina-login {
            padding: 22px 15px;
        }

        .login-card {
            padding: 32px 23px 25px;
            border-radius: 19px;
        }

        .bienvenida h1 {
            font-size: 1.75rem;
        }

        .instruction-text {
            font-size: 0.78rem;
        }

        .decoracion-tres {
            right: -70px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .contenido-login,
        .mensaje,
        .spinner {
            animation: none;
        }

        .login-card,
        .btn-submit,
        input {
            transition: none;
        }
    }
.registro-enlace {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    margin-top: 20px;
    font-size: 0.85rem;
    flex-wrap: wrap;
}

.registro-enlace span {
    color: #718096;
}

.registro-enlace a {
    color: #008cbd;
    font-weight: 750;
    text-decoration: none;
    transition: color 0.2s ease;
}

.registro-enlace a:hover {
    color: #0b8457;
    text-decoration: underline;
}
</style>

