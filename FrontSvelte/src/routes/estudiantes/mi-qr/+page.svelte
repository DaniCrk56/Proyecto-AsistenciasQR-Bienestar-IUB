
<script>
    import { onMount } from 'svelte';
    import QRCode from 'qrcode';

    const URL_BASE = 'https://proyecto-asistenciasqr-bienestar-iub.onrender.com';

    let estudiante = {
        nombre: 'Cargando...'
    };

    let inscripciones = [];
    let qrImagen = '';
    let mensaje = '';
    let menuAbierto = false;
    let cargando = true;
    let mostrarModal = false;
    let inscripcionSeleccionada = null;
    let generandoQR = false;

    onMount(async () => {
        const usuarioGuardado = localStorage.getItem('usuario');

        if (!usuarioGuardado) {
            estudiante.nombre = 'No se encontró el usuario';
            mensaje = 'Inicia sesión para consultar tus códigos QR.';
            cargando = false;
            return;
        }

        try {
            const usuario = JSON.parse(usuarioGuardado);

            estudiante.nombre =
                `${usuario.nombres || ''} ${usuario.apellidos || ''}`.trim();

            if (!usuario.id) {
                mensaje = 'No se encontró el identificador del estudiante.';
                cargando = false;
                return;
            }

            const respuesta = await fetch(
                `${URL_BASE}/inscripciones/estudiante/${usuario.id}`
            );

            if (!respuesta.ok) {
                throw new Error('No fue posible consultar las inscripciones.');
            }

            const datos = await respuesta.json();

            inscripciones = Array.isArray(datos) ? datos : [];

        } catch (error) {
            console.error('Error consultando inscripciones:', error);
            mensaje = 'No fue posible cargar tus inscripciones. Intenta nuevamente.';
        } finally {
            cargando = false;
        }
    });

    async function verQR(inscripcion) {
        inscripcionSeleccionada = inscripcion;
        qrImagen = '';
        mensaje = '';
        mostrarModal = true;
        generandoQR = true;

        try {
            qrImagen = await QRCode.toDataURL(inscripcion.codigo_qr, {
                width: 400,
                margin: 2,
                errorCorrectionLevel: 'H',
                color: {
                    dark: '#142044',
                    light: '#FFFFFF'
                }
            });
        } catch (error) {
            console.error('Error generando QR:', error);
            mensaje = 'No fue posible generar el código QR.';
        } finally {
            generandoQR = false;
        }
    }

    function cerrarModal() {
        mostrarModal = false;
        inscripcionSeleccionada = null;
        qrImagen = '';
        mensaje = '';
    }

    function descargarQR() {
        if (!qrImagen || !inscripcionSeleccionada) {
            mensaje = 'El código QR todavía no está disponible.';
            return;
        }

        const enlace = document.createElement('a');
        enlace.href = qrImagen;
        enlace.download = `QR-Inscripcion-${inscripcionSeleccionada.id}.png`;
        enlace.click();

        mensaje = 'Tu código QR se descargó correctamente.';
    }

    function formatoFecha(fecha) {
        if (!fecha) return 'Fecha no disponible';

        const partes = fecha.split('-');

        if (partes.length !== 3) return fecha;

        return `${partes[2]}/${partes[1]}/${partes[0]}`;
    }

    function formatoHora(hora) {
        if (!hora) return 'Hora no disponible';

        return hora.substring(0, 5);
    }

    function nombreArchivo(nombre) {
        return (nombre || 'evento')
            .replace(/[^a-zA-Z0-9]/g, '-')
            .replace(/-+/g, '-');
    }
</script>

<svelte:head>
    <title>Mi código QR | Bienestar Universitario IUB</title>
    <meta name="description" content="Consulta los códigos QR de tus inscripciones a eventos universitarios." />
    <link
        href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900;1000&display=swap"
        rel="stylesheet"
    />
</svelte:head>

<div class="pagina">

    <!-- ENCABEZADO PRINCIPAL -->
    <header class="encabezado">
        <a href="/estudiantes/eventos" class="identidad">
            <div class="logo-contenedor">
                <img src="/LogoIUB.png" alt="Logo IUB" />
            </div>

            <div class="identidad-texto">
                <strong>BIENESTAR</strong>
                <span>UNIVERSITARIO</span>
            </div>
        </a>

        <button
            class="boton-menu"
            onclick={() => menuAbierto = !menuAbierto}
            aria-label={menuAbierto ? 'Cerrar menú' : 'Abrir menú'}
            aria-expanded={menuAbierto}
        >
            {#if menuAbierto}
                ✕
            {:else}
                ☰
            {/if}
        </button>

        <nav class:abierto={menuAbierto} class="navegacion">
            <a
                href="/estudiantes/eventos"
                class="enlace"
                onclick={() => menuAbierto = false}
            >
                <span>▦</span>
                Eventos
            </a>

            <a
                href="/estudiantes/mi-qr"
                class="enlace activo"
                onclick={() => menuAbierto = false}
            >
                <span>▣</span>
                Mi código QR
            </a>

            <a
                href="/estudiantes/perfil"
                class="enlace"
                onclick={() => menuAbierto = false}
            >
                <span>●</span>
                Mi perfil
            </a>
        </nav>
    </header>

    <main>

        <!-- PRESENTACIÓN -->
        <section class="presentacion">
            <div class="presentacion-contenido">
                <span class="etiqueta">
                    <span></span>
                    IDENTIFICACIÓN UNIVERSITARIA
                </span>

                <h1>Mi código <span>QR.</span></h1>

                <p>
                    Consulta los códigos QR de tus inscripciones y presenta
                    el correspondiente para registrar tu asistencia en cada evento.
                </p>
            </div>

            <div class="presentacion-decoracion">
                <div class="circulo circulo-1"></div>
                <div class="circulo circulo-2"></div>
                <span>QR</span>
            </div>
        </section>

        <!-- CONTENIDO -->
        <section class="contenido">

            <div class="titulo-seccion">
                <div>
                    <span class="subtitulo">TUS INSCRIPCIONES</span>
                    <h2>Mis eventos inscritos</h2>
                    <p>
                        Selecciona un evento para consultar y descargar
                        tu código QR de asistencia.
                    </p>
                </div>

                <div class="estado">
                    <span></span>
                    {inscripciones.length} {inscripciones.length === 1 ? 'inscripción' : 'inscripciones'}
                </div>
            </div>

            {#if cargando}
                <div class="mensaje-estado">
                    <div class="cargando-circulo"></div>
                    <h3>Consultando tus inscripciones...</h3>
                    <p>Estamos buscando los eventos en los que estás registrado.</p>
                </div>

            {:else if mensaje && inscripciones.length === 0}
                <div class="mensaje-estado">
                    <div class="icono-estado">!</div>
                    <h3>No fue posible cargar tus eventos</h3>
                    <p>{mensaje}</p>
                </div>

            {:else if inscripciones.length === 0}
                <div class="mensaje-estado">
                    <div class="icono-estado">▦</div>
                    <h3>Aún no tienes inscripciones</h3>
                    <p>
                        Cuando te inscribas a un evento de Bienestar Universitario,
                        podrás consultar aquí su respectivo código QR.
                    </p>

                    <a href="/estudiantes/eventos" class="boton-eventos">
                        Explorar eventos
                    </a>
                </div>

            {:else}
                <div class="eventos-grid">

                    {#each inscripciones as inscripcion (inscripcion.id)}
                        <article class="tarjeta-evento">

                            <div class="evento-cabecera">
                                <div class="evento-icono">▦</div>

                                <span class="evento-estado">
                                    <span></span>
                                    Inscrito
                                </span>
                            </div>

                            <div class="evento-contenido">
                                <span class="evento-etiqueta">EVENTO UNIVERSITARIO</span>

                                <h3>{inscripcion.nombre_evento}</h3>

                                <p class="evento-descripcion">
                                    {inscripcion.descripcion || 'Participa en esta actividad de Bienestar Universitario.'}
                                </p>

                                <div class="evento-datos">
                                    <div>
                                        <span class="dato-icono">▣</span>
                                        <span>{formatoFecha(inscripcion.fecha)}</span>
                                    </div>

                                    <div>
                                        <span class="dato-icono">◷</span>
                                        <span>
                                            {formatoHora(inscripcion.hora_inicio)}
                                            - {formatoHora(inscripcion.hora_fin)}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div class="evento-pie">
                                <span>Inscripción #{inscripcion.id}</span>

                                <button
                                    class="boton-ver-qr"
                                    onclick={() => verQR(inscripcion)}
                                >
                                    Ver mi QR
                                    <span>→</span>
                                </button>
                            </div>

                        </article>
                    {/each}

                </div>
            {/if}

            <!-- INSTRUCCIONES -->
            <section class="instrucciones">
                <div class="instrucciones-titulo">
                    <span class="subtitulo">FÁCIL Y RÁPIDO</span>
                    <h2>¿Cómo utilizar tu código QR?</h2>
                </div>

                <div class="pasos">

                    <div class="paso">
                        <div class="paso-numero">01</div>
                        <div class="paso-icono">▣</div>
                        <h3>Selecciona tu evento</h3>
                        <p>Busca el evento al que te inscribiste y pulsa Ver mi QR.</p>
                    </div>

                    <div class="paso">
                        <div class="paso-numero">02</div>
                        <div class="paso-icono">▤</div>
                        <h3>Presenta tu código</h3>
                        <p>Muestra el código QR correspondiente al evento.</p>
                    </div>

                    <div class="paso">
                        <div class="paso-numero">03</div>
                        <div class="paso-icono">✓</div>
                        <h3>Registra tu asistencia</h3>
                        <p>El personal autorizado escaneará tu código para validar tu ingreso.</p>
                    </div>

                </div>
            </section>

        </section>

    </main>

    <!-- MODAL DEL QR -->
    {#if mostrarModal && inscripcionSeleccionada}
        <div
            class="modal-fondo"
            role="presentation"
            onclick={(evento) => {
                if (evento.target === evento.currentTarget) cerrarModal();
            }}
        >
            <div class="modal-qr" role="dialog" aria-modal="true" aria-labelledby="titulo-modal-qr">

                <div class="modal-cabecera">
                    <div>
                        <span class="subtitulo">TU IDENTIFICACIÓN PARA EL EVENTO</span>
                        <h2 id="titulo-modal-qr">Mi código QR</h2>
                    </div>

                    <button
                        class="boton-cerrar"
                        onclick={cerrarModal}
                        aria-label="Cerrar ventana"
                    >
                        ✕
                    </button>
                </div>

                <div class="modal-evento">
                    <span>EVENTO</span>
                    <strong>{inscripcionSeleccionada.nombre_evento}</strong>
                    <small>
                        {formatoFecha(inscripcionSeleccionada.fecha)}
                        · {formatoHora(inscripcionSeleccionada.hora_inicio)}
                    </small>
                </div>

                <div class="qr-modal-contenedor">
                    {#if generandoQR}
                        <div class="qr-cargando">
                            Generando código QR...
                        </div>
                    {:else if qrImagen}
                        <img
                            src={qrImagen}
                            alt="Código QR de la inscripción al evento"
                            class="qr-imagen"
                        />
                    {:else}
                        <div class="qr-cargando">
                            No se pudo generar el código QR.
                        </div>
                    {/if}
                </div>

                <p class="modal-indicacion">
                    Presenta este código al personal encargado para registrar
                    tu asistencia al evento.
                </p>

                <button
                    class="boton-descargar"
                    onclick={descargarQR}
                    disabled={!qrImagen}
                >
                    <span>↓</span>
                    Descargar código QR
                </button>

                {#if mensaje}
                    <div class="mensaje">{mensaje}</div>
                {/if}

                <button class="boton-volver" onclick={cerrarModal}>
                    Cerrar
                </button>

            </div>
        </div>
    {/if}

    <!-- FOOTER -->
    <footer>
        <div class="footer-contenido">
            <div class="footer-identidad">
                <img src="/LogoIUB.png" alt="Logo IUB" />

                <div>
                    <strong>Bienestar Universitario</strong>
                    <span>Institución Universitaria de Barranquilla</span>
                </div>
            </div>

            <p>Promoviendo el bienestar y la integración de nuestra comunidad.</p>
        </div>

        <div class="footer-final">
            <span>© 2026 Institución Universitaria de Barranquilla</span>
            <span>Portal de Bienestar Universitario</span>
        </div>
    </footer>

</div>

<style>
    :global(*) {
        box-sizing: border-box;
    }

    :global(body) {
        margin: 0;
        background: #f5f7fb;
        color: #17213b;
        font-family: 'Nunito', sans-serif;
    }

    .pagina {
        min-height: 100vh;
        overflow: hidden;
    }

    /* ENCABEZADO */

    .encabezado {
        width: 100%;
        min-height: 88px;
        padding: 12px 7%;
        background: #142044;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 25px;
        position: relative;
        z-index: 20;
        animation: entradaQRArriba .7s ease both;
    }

    .identidad {
        display: flex;
        align-items: center;
        gap: 13px;
        text-decoration: none;
    }

    .logo-contenedor {
        width: 57px;
        height: 57px;
        background: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 5px;
    }

    .logo-contenedor img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .identidad-texto {
        display: flex;
        flex-direction: column;
        color: white;
        line-height: 1.05;
    }

    .identidad-texto strong {
        font-size: 20px;
        font-weight: 1000;
        letter-spacing: .5px;
    }

    .identidad-texto span {
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 2px;
    }

    .navegacion {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 35px;
    }

    .enlace {
        color: #e2e7f4;
        text-decoration: none;
        font-size: 16px;
        font-weight: 900;
        display: flex;
        align-items: center;
        gap: 9px;
        transition: .2s;
        position: relative;
        padding-bottom: 7px;
    }

    .enlace span {
        font-size: 20px;
    }

    .enlace:hover,
    .enlace.activo {
        color: #f5ca24;
    }

    .enlace::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 2px;
        background: #f5ca24;
        transform: scaleX(0);
        transform-origin: left;
        transition: transform .3s ease;
    }

    .enlace:hover::after,
    .enlace.activo::after {
        transform: scaleX(1);
    }

    .boton-menu {
        display: none;
    }

    /* PRESENTACIÓN */

    .presentacion {
        width: 92%;
        max-width: 1450px;
        min-height: 260px;
        margin: 28px auto 0;
        padding: 45px 7%;
        border-radius: 23px;
        background: linear-gradient(110deg, #111c3b, #1d4d8c);
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        box-shadow: 0 12px 30px rgba(17, 28, 59, .15);
        animation: entradaQRAbajo .8s ease both;
    }

    .presentacion-contenido {
        position: relative;
        z-index: 2;
        max-width: 600px;
    }

    .etiqueta {
        display: flex;
        align-items: center;
        gap: 9px;
        color: #f5ca24;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 2px;
    }

    .etiqueta span {
        width: 23px;
        height: 2px;
        background: #f5ca24;
    }

    .presentacion h1 {
        color: white;
        font-size: 45px;
        font-weight: 1000;
        letter-spacing: -1px;
        margin: 15px 0 8px;
    }

    .presentacion h1 span {
        color: #f5ca24;
    }

    .presentacion p {
        color: #d5deee;
        font-size: 13px;
        line-height: 1.8;
        max-width: 460px;
        margin: 0;
    }

    .presentacion-decoracion {
        position: absolute;
        width: 250px;
        height: 250px;
        right: 10%;
        top: 50%;
        transform: translateY(-50%);
        display: grid;
        place-items: center;
    }

    .circulo {
        position: absolute;
        border: 1px solid rgba(255,255,255,.2);
        border-radius: 50%;
    }

    .circulo-1 {
        width: 240px;
        height: 240px;
        animation: flotarQR 6s ease-in-out infinite;
    }

    .circulo-2 {
        width: 175px;
        height: 175px;
        border-color: rgba(245,202,36,.5);
        animation: flotarQR 5s ease-in-out infinite reverse;
    }

    .presentacion-decoracion > span {
        color: white;
        font-size: 55px;
        font-weight: 1000;
        transform: rotate(-10deg);
        animation: girarQR 5s ease-in-out infinite;
    }

    /* CONTENIDO */

    .contenido {
        max-width: 1200px;
        width: 88%;
        margin: 60px auto;
    }

    .titulo-seccion {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        margin-bottom: 30px;
    }

    .subtitulo {
        color: #b18c0b;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 2px;
    }

    .titulo-seccion h2 {
        color: #142044;
        font-size: 28px;
        font-weight: 1000;
        margin: 8px 0 5px;
    }

    .titulo-seccion p {
        color: #7d879c;
        font-size: 12px;
        margin: 0;
    }

    .estado {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #fff7dc;
        color: #967400;
        padding: 11px 16px;
        border-radius: 30px;
        font-size: 10px;
        font-weight: 900;
        white-space: nowrap;
    }

    .estado span {
        width: 7px;
        height: 7px;
        background: #d5a900;
        border-radius: 50%;
    }

    /* TARJETAS DE EVENTOS */

    .eventos-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 24px;
    }

    .tarjeta-evento {
        background: white;
        border: 1px solid #e9edf4;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(20,32,68,.06);
        transition: transform .3s ease, box-shadow .3s ease;
        animation: entradaQRAbajo .7s ease both;
    }

    .tarjeta-evento:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 35px rgba(20,32,68,.12);
    }

    .evento-cabecera {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
    }

    .evento-icono {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: #edf3fb;
        color: #1d4b8c;
        display: grid;
        place-items: center;
        font-size: 24px;
        font-weight: 900;
    }

    .evento-estado {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 8px 12px;
        border-radius: 20px;
        background: #e9f8ef;
        color: #21834b;
        font-size: 10px;
        font-weight: 900;
    }

    .evento-estado span {
        width: 7px;
        height: 7px;
        background: #27ae60;
        border-radius: 50%;
    }

    .evento-etiqueta {
        color: #b18c0b;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1.5px;
    }

    .evento-contenido h3 {
        color: #142044;
        font-size: 21px;
        font-weight: 1000;
        margin: 8px 0;
    }

    .evento-descripcion {
        color: #8992a5;
        font-size: 12px;
        line-height: 1.7;
        min-height: 40px;
        margin: 0 0 20px;
    }

    .evento-datos {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 16px 0;
        border-top: 1px solid #edf0f5;
    }

    .evento-datos div {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #536580;
        font-size: 11px;
        font-weight: 800;
    }

    .dato-icono {
        color: #1d4b8c;
        font-size: 17px;
    }

    .evento-pie {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        border-top: 1px solid #edf0f5;
        padding-top: 17px;
        margin-top: 5px;
    }

    .evento-pie > span {
        color: #929bad;
        font-size: 10px;
        font-weight: 900;
    }

    .boton-ver-qr {
        border: none;
        border-radius: 30px;
        padding: 12px 18px;
        background: linear-gradient(100deg, #142044, #1e4d91);
        color: white;
        font-family: inherit;
        font-size: 11px;
        font-weight: 1000;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: .25s ease;
    }

    .boton-ver-qr:hover {
        background: #f5ca24;
        color: #142044;
        transform: translateY(-3px);
    }

    .boton-ver-qr span {
        font-size: 18px;
    }

    /* MENSAJES DE ESTADO */

    .mensaje-estado {
        width: 100%;
        padding: 55px 25px;
        background: white;
        border: 1px solid #e9edf4;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(20,32,68,.05);
        animation: entradaQRAbajo .6s ease both;
    }

    .mensaje-estado h3 {
        color: #142044;
        font-size: 20px;
        font-weight: 1000;
        margin: 15px 0 8px;
    }

    .mensaje-estado p {
        color: #8992a5;
        font-size: 12px;
        line-height: 1.7;
        max-width: 480px;
        margin: auto;
    }

    .icono-estado {
        width: 60px;
        height: 60px;
        margin: auto;
        border-radius: 18px;
        display: grid;
        place-items: center;
        background: #edf3fb;
        color: #1d4b8c;
        font-size: 30px;
        font-weight: 1000;
    }

    .cargando-circulo {
        width: 38px;
        height: 38px;
        margin: auto;
        border: 4px solid #e5eaf2;
        border-top-color: #1d4b8c;
        border-radius: 50%;
        animation: girarCargando .8s linear infinite;
    }

    .boton-eventos {
        display: inline-flex;
        margin-top: 22px;
        padding: 13px 22px;
        border-radius: 30px;
        background: linear-gradient(100deg, #142044, #1e4d91);
        color: white;
        text-decoration: none;
        font-size: 11px;
        font-weight: 1000;
        transition: .25s ease;
    }

    .boton-eventos:hover {
        background: #f5ca24;
        color: #142044;
        transform: translateY(-3px);
    }

    /* MODAL QR */

    .modal-fondo {
        position: fixed;
        inset: 0;
        z-index: 200;
        background: rgba(10, 18, 40, .75);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        overflow-y: auto;
        animation: aparecerModal .25s ease both;
    }

    .modal-qr {
        width: 100%;
        max-width: 460px;
        max-height: 95vh;
        overflow-y: auto;
        background: white;
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 20px 60px rgba(0,0,0,.25);
        animation: entradaQRAbajo .35s ease both;
    }

    .modal-cabecera {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 15px;
        margin-bottom: 20px;
    }

    .modal-cabecera h2 {
        color: #142044;
        font-size: 25px;
        font-weight: 1000;
        margin: 7px 0 0;
    }

    .boton-cerrar {
        width: 36px;
        height: 36px;
        flex-shrink: 0;
        border: none;
        border-radius: 50%;
        background: #edf0f5;
        color: #142044;
        font-size: 17px;
        font-weight: 900;
        cursor: pointer;
        transition: .2s;
    }

    .boton-cerrar:hover {
        background: #f5ca24;
        transform: rotate(90deg);
    }

    .modal-evento {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding: 15px;
        background: #edf3fb;
        border-radius: 13px;
        text-align: center;
    }

    .modal-evento span {
        color: #b18c0b;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1.5px;
    }

    .modal-evento strong {
        color: #142044;
        font-size: 16px;
        font-weight: 1000;
    }

    .modal-evento small {
        color: #536580;
        font-size: 10px;
        font-weight: 800;
    }

    .qr-modal-contenedor {
        width: 250px;
        height: 250px;
        padding: 12px;
        margin: 22px auto;
        display: flex;
        justify-content: center;
        align-items: center;
        background: white;
        border: 1px solid #e5eaf2;
        border-radius: 14px;
        box-shadow: 0 5px 18px rgba(20,32,68,.06);
        animation: aparecerCodigo .5s ease both;
    }

    .qr-imagen {
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
    }

    .qr-cargando {
        color: #8992a5;
        font-size: 12px;
        font-weight: 900;
        text-align: center;
    }

    .modal-indicacion {
        color: #7d879c;
        font-size: 11px;
        line-height: 1.7;
        text-align: center;
        margin: 0 0 18px;
    }

    .boton-descargar {
        width: 100%;
        padding: 15px;
        border: none;
        border-radius: 30px;
        background: linear-gradient(100deg, #142044, #1e4d91);
        color: white;
        font-family: inherit;
        font-size: 12px;
        font-weight: 1000;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        box-shadow: 0 7px 17px rgba(20,32,68,.17);
        transition: .25s ease;
    }

    .boton-descargar:hover:not(:disabled) {
        background: #f5ca24;
        color: #142044;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(245,202,36,.25);
    }

    .boton-descargar:disabled {
        opacity: .5;
        cursor: not-allowed;
    }

    .boton-descargar span {
        font-size: 20px;
    }

    .boton-volver {
        width: 100%;
        margin-top: 12px;
        padding: 12px;
        border: 1px solid #e5eaf2;
        border-radius: 30px;
        background: white;
        color: #536580;
        font-family: inherit;
        font-size: 11px;
        font-weight: 900;
        cursor: pointer;
        transition: .2s;
    }

    .boton-volver:hover {
        background: #edf3fb;
        color: #142044;
    }

    .mensaje {
        padding: 12px;
        margin-top: 14px;
        background: #edf3fb;
        border-radius: 10px;
        color: #234878;
        font-size: 11px;
        line-height: 1.6;
        animation: entradaQRAbajo .4s ease both;
    }

    /* INSTRUCCIONES */

    .instrucciones {
        margin-top: 75px;
    }

    .instrucciones-titulo {
        text-align: center;
    }

    .instrucciones-titulo h2 {
        color: #142044;
        font-size: 27px;
        font-weight: 1000;
        margin: 10px 0 30px;
    }

    .pasos {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }

    .paso {
        position: relative;
        padding: 25px;
        border-radius: 18px;
        background: white;
        border: 1px solid #e9edf4;
        box-shadow: 0 7px 20px rgba(20,32,68,.04);
        transition: transform .3s ease, box-shadow .3s ease;
        animation: entradaQRAbajo .8s ease both;
    }

    .paso:nth-child(1) {
        animation-delay: .1s;
    }

    .paso:nth-child(2) {
        animation-delay: .2s;
    }

    .paso:nth-child(3) {
        animation-delay: .3s;
    }

    .paso:hover {
        transform: translateY(-7px);
        box-shadow: 0 15px 30px rgba(20,32,68,.10);
    }

    .paso-numero {
        position: absolute;
        right: 20px;
        top: 15px;
        color: #e7ebf3;
        font-size: 29px;
        font-weight: 1000;
    }

    .paso-icono {
        width: 47px;
        height: 47px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        background: #edf3fb;
        color: #1d4b8c;
        font-size: 23px;
        font-weight: 900;
        transition: transform .3s ease, background .3s ease;
    }

    .paso:hover .paso-icono {
        transform: scale(1.12) rotate(-5deg);
        background: #dceafa;
    }

    .paso h3 {
        color: #142044;
        font-size: 16px;
        font-weight: 1000;
        margin: 18px 0 8px;
    }

    .paso p {
        color: #8992a5;
        font-size: 11px;
        line-height: 1.7;
        margin: 0;
    }

    /* FOOTER */

    footer {
        background: #101a36;
        color: white;
        padding: 35px 6% 0;
        animation: entradaQRAbajo .8s ease both;
    }

    .footer-contenido {
        max-width: 1200px;
        margin: auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        padding-bottom: 28px;
    }

    .footer-identidad {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .footer-identidad img {
        width: 58px;
        height: 48px;
        object-fit: contain;
        background: white;
        border-radius: 10px;
        padding: 4px;
    }

    .footer-identidad div {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .footer-identidad strong {
        font-size: 13px;
        font-weight: 1000;
    }

    .footer-identidad span {
        color: #aebbd2;
        font-size: 10px;
    }

    .footer-contenido > p {
        color: #aebbd2;
        font-size: 11px;
    }

    .footer-final {
        border-top: 1px solid rgba(255,255,255,.1);
        max-width: 1200px;
        margin: auto;
        padding: 17px 0;
        display: flex;
        justify-content: space-between;
        color: #8f9bb2;
        font-size: 10px;
    }

    /* ANIMACIONES */

    @keyframes entradaQRArriba {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes entradaQRAbajo {
        from {
            opacity: 0;
            transform: translateY(22px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes aparecerCodigo {
        from {
            opacity: 0;
            transform: scale(.88);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes flotarQR {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.08);
        }
    }

    @keyframes girarQR {
        0%, 100% {
            transform: rotate(-10deg);
        }
        50% {
            transform: rotate(5deg);
        }
    }

    @keyframes girarCargando {
        to {
            transform: rotate(360deg);
        }
    }

    @keyframes aparecerModal {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    /* RESPONSIVE */

    @media (max-width: 850px) {
        .eventos-grid {
            grid-template-columns: 1fr;
        }

        .presentacion-decoracion {
            right: 2%;
            opacity: .4;
        }
    }

    @media (max-width: 700px) {
        .encabezado {
            min-height: 75px;
            padding: 10px 5%;
            gap: 10px;
            flex-wrap: wrap;
        }

        .logo-contenedor {
            width: 45px;
            height: 45px;
        }

        .identidad {
            gap: 9px;
        }

        .identidad-texto strong {
            font-size: 16px;
        }

        .identidad-texto span {
            font-size: 10px;
            letter-spacing: 1.3px;
        }

        .boton-menu {
            display: block;
            margin-left: auto;
            border: none;
            background: transparent;
            color: white;
            font-size: 27px;
            font-weight: 700;
            cursor: pointer;
            padding: 5px 8px;
        }

    
.navegacion {
    display: flex;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    width: 100%;
    background: #142044;
    padding: 10px 5% 18px;
    flex-direction: column;
    align-items: stretch;
    gap: 5px;
    z-index: 100;

    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transform: translateY(-12px);

    box-shadow: 0 10px 20px rgba(0,0,0,.2);

    transition:
        opacity .3s ease,
        transform .35s ease,
        visibility .3s ease;
}

.navegacion.abierto {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: translateY(0);
}

.enlace {
    transition: background .25s ease, color .25s ease;
}

.enlace:hover,
.enlace.activo {
    background: rgba(245, 202, 36, .10);
    color: #f5ca24;
}

.enlace::after {
    display: none;
}

        .enlace {
            width: 100%;
            padding: 13px 10px;
            font-size: 14px;
            gap: 12px;
            border-radius: 8px;
        }

        .enlace span {
            font-size: 19px;
        }

        .presentacion {
            width: 92%;
            min-height: 230px;
            padding: 30px 25px;
            margin-top: 16px;
        }

        .presentacion h1 {
            font-size: 35px;
        }

        .presentacion p {
            font-size: 11px;
            max-width: 280px;
        }

        .presentacion-decoracion {
            right: -130px;
            opacity: .25;
        }

        .contenido {
            width: 90%;
            margin: 40px auto;
        }

        .titulo-seccion {
            align-items: flex-start;
            flex-direction: column;
        }

        .titulo-seccion h2 {
            font-size: 24px;
        }

        .pasos {
            grid-template-columns: 1fr;
        }

        .instrucciones-titulo h2 {
            font-size: 23px;
        }

        .footer-contenido {
            align-items: flex-start;
            flex-direction: column;
        }

        .footer-final {
            flex-direction: column;
            gap: 10px;
        }

        .modal-qr {
            padding: 22px;
        }

        .qr-modal-contenedor {
            width: 225px;
            height: 225px;
        }
    }

    @media (max-width: 400px) {
        .evento-pie {
            align-items: flex-start;
            flex-direction: column;
        }

        .boton-ver-qr {
            width: 100%;
            justify-content: center;
        }

        .modal-cabecera h2 {
            font-size: 21px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation: none !important;
            transition: none !important;
        }
    }
</style>
