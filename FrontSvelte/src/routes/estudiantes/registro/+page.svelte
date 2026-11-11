
<script>
    let nombres = '';
    let apellidos = '';
    let tipo_documento = '';
    let numero_documento = '';
    let correo_institucional = '';
    let programa = '';
    let password = '';
    let confirmar_password = '';

    let mensaje = '';
    let error = false;

    function manejarRegistro(evento) {
        evento.preventDefault();

        mensaje = '';
        error = false;

        if (password !== confirmar_password) {
            error = true;
            mensaje = 'Las contraseñas no coinciden.';
            return;
        }

        mensaje = 'Formulario listo. En el siguiente paso conectaremos el registro con el sistema.';
    }
</script>

<svelte:head>
    <title>Crear cuenta | Bienestar Universitario IUB</title>
    <meta name="description" content="Registro de estudiantes en el sistema de Bienestar Universitario." />
</svelte:head>

<div class="pagina-registro">

    <div class="decoracion decoracion-uno"></div>
    <div class="decoracion decoracion-dos"></div>
    <div class="decoracion decoracion-tres"></div>

    <div class="contenido-registro">

        <div class="registro-card">

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
                <h1>¡Crea tu cuenta!</h1>
                <p>Regístrate para participar en los eventos universitarios.</p>
            </div>

            <div class="instruction-text">
                <span class="punto"></span>
                Completa tus datos para registrarte en el sistema
            </div>

            {#if mensaje}
                <div class="mensaje" class:error-msg={error} class:success-msg={!error}>
                    <span>{error ? '⚠' : '✓'}</span>
                    {mensaje}
                </div>
            {/if}

            <form onsubmit={manejarRegistro}>

                <div class="form-grid">

                    <div class="form-group">
                        <label for="nombres">Nombres</label>

                        <div class="input-contenedor">
                            <span class="icono-input">👤</span>
                            <input
                                type="text"
                                id="nombres"
                                bind:value={nombres}
                                placeholder="Tus nombres"
                                autocomplete="given-name"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="apellidos">Apellidos</label>

                        <div class="input-contenedor">
                            <span class="icono-input">👤</span>
                            <input
                                type="text"
                                id="apellidos"
                                bind:value={apellidos}
                                placeholder="Tus apellidos"
                                autocomplete="family-name"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="tipo_documento">Tipo de documento</label>

                        <div class="input-contenedor">
                            <span class="icono-input">▤</span>
                            <select
                                id="tipo_documento"
                                bind:value={tipo_documento}
                                required
                            >
                                <option value="" disabled>Selecciona tu documento</option>
                                <option value="CC">Cédula de ciudadanía</option>
                                <option value="TI">Tarjeta de identidad</option>
                                <option value="CE">Cédula de extranjería</option>
                                <option value="PAS">Pasaporte</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="numero_documento">Número de documento</label>

                        <div class="input-contenedor">
                            <span class="icono-input">#</span>
                            <input
                                type="text"
                                id="numero_documento"
                                bind:value={numero_documento}
                                placeholder="Número de documento"
                                autocomplete="off"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-group completo">
                        <label for="correo">Correo institucional</label>

                        <div class="input-contenedor">
                            <span class="icono-input">✉</span>
                            <input
                                type="email"
                                id="correo"
                                bind:value={correo_institucional}
                                placeholder="tucorreo@unibarranquilla.edu.co"
                                autocomplete="email"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-group completo">
                        <label for="programa">Programa académico</label>

                        <div class="input-contenedor">
                            <span class="icono-input">🎓</span>
                            <input
                                type="text"
                                id="programa"
                                bind:value={programa}
                                placeholder="Escribe tu programa académico"
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
                                placeholder="Crea una contraseña"
                                autocomplete="new-password"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="confirmar_password">Confirmar contraseña</label>

                        <div class="input-contenedor">
                            <span class="icono-input">🔒</span>
                            <input
                                type="password"
                                id="confirmar_password"
                                bind:value={confirmar_password}
                                placeholder="Repite tu contraseña"
                                autocomplete="new-password"
                                required
                            />
                        </div>
                    </div>

                </div>

                <button type="submit" class="btn-submit">
                    Crear mi cuenta
                    <span class="flecha">→</span>
                </button>

            </form>

            <div class="registro-enlace">
                <span>¿Ya tienes una cuenta?</span>
                <a href="/">Inicia sesión</a>
            </div>

            <div class="linea-inferior"></div>

            <div class="mensaje-seguridad">
                <span>🔐</span>
                Registro exclusivo para estudiantes institucionales
            </div>

        </div>

        <footer class="footer-registro">
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

    .pagina-registro {
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

    .contenido-registro {
        width: 100%;
        max-width: 720px;
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

    .registro-card {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(15, 55, 80, 0.13);
        border: 1px solid rgba(255, 255, 255, 0.9);
        padding: 35px 38px 30px;
        width: 100%;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .registro-card:hover {
        transform: translateY(-3px);
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
        margin-bottom: 20px;
        text-align: center;
    }

    .logo-contenedor {
        width: 110px;
        height: 75px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }

    .logo-auth {
        max-height: 75px;
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
        margin: 13px 0 10px;
    }

    .etiqueta-sistema {
        color: #008cbd;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 2px;
    }

    .bienvenida {
        text-align: center;
        margin-bottom: 23px;
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
        margin-bottom: 20px;
    }

    .punto {
        width: 8px;
        height: 8px;
        background: #00aeef;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        column-gap: 18px;
    }

    .form-group {
        margin-bottom: 18px;
        min-width: 0;
    }

    .completo {
        grid-column: 1 / -1;
    }

    label {
        display: block;
        margin-bottom: 8px;
        font-weight: 700;
        color: #34495e;
        font-size: 0.86rem;
    }

    .input-contenedor {
        position: relative;
        display: flex;
        align-items: center;
    }

    .icono-input {
        position: absolute;
        left: 14px;
        font-size: 0.95rem;
        z-index: 1;
        opacity: 0.65;
        pointer-events: none;
    }

    input,
    select {
        width: 100%;
        min-width: 0;
        padding: 13px 12px 13px 42px;
        border: 1px solid #dce5ed;
        border-radius: 11px;
        font-size: 0.87rem;
        background: #f8fbfd;
        color: #263746;
        outline: none;
        transition: all 0.25s ease;
        font-family: inherit;
    }

    input::placeholder {
        color: #a3b0bc;
    }

    select {
        appearance: none;
        cursor: pointer;
    }

    select:invalid {
        color: #a3b0bc;
    }

    input:focus,
    select:focus {
        border-color: #00aeef;
        background: #ffffff;
        box-shadow: 0 0 0 4px rgba(0, 174, 239, 0.11);
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
        margin-top: 5px;
        box-shadow: 0 7px 17px rgba(0, 174, 239, 0.23);
        transition: all 0.25s ease;
    }

    .btn-submit:hover {
        background: linear-gradient(110deg, #009bd6, #066d94);
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(0, 174, 239, 0.32);
    }

    .btn-submit:active {
        transform: scale(0.98);
    }

    .flecha {
        font-size: 1.25rem;
        transition: transform 0.25s ease;
    }

    .btn-submit:hover .flecha {
        transform: translateX(5px);
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

    .linea-inferior {
        height: 1px;
        background: #edf1f5;
        margin: 23px 0 17px;
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

    .footer-registro {
        text-align: center;
        margin-top: 24px;
        color: #567184;
        display: flex;
        flex-direction: column;
        gap: 5px;
        font-size: 0.78rem;
    }

    .footer-registro p {
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

    @media (max-width: 600px) {
        .pagina-registro {
            padding: 22px 14px;
        }

        .registro-card {
            padding: 30px 21px 25px;
            border-radius: 19px;
        }

        .form-grid {
            grid-template-columns: 1fr;
        }

        .completo {
            grid-column: auto;
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
        .contenido-registro,
        .mensaje {
            animation: none;
        }

        .registro-card,
        .btn-submit,
        input,
        select {
            transition: none;
        }
    }
</style>
