
<script>
    import { onMount } from 'svelte';

    let estudiante = {
        nombre: 'Cargando...',
        documento: 'No registrado',
        tipoDocumento: 'No registrado',
        correo: 'No registrado',
        programa: 'No registrado',
        codigo: 'No registrado'
    };

    let menuAbierto = false;
let mostrarConfirmacion = false;
function cerrarSesion() {
    mostrarConfirmacion = false;
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    window.location.href = '/';
}

function cancelarCierre() {
    mostrarConfirmacion = false;
}

    onMount(() => {
        const usuarioGuardado = localStorage.getItem('usuario');

        if (usuarioGuardado) {
            try {
                const usuario = JSON.parse(usuarioGuardado);

                estudiante = {
                    nombre: `${usuario.nombres || ''} ${usuario.apellidos || ''}`.trim() || 'Nombre no disponible',
                    documento: usuario.numero_documento || 'No registrado',
                    tipoDocumento: usuario.tipo_documento || 'No registrado',
                    correo: usuario.correo_institucional || 'No registrado',
                    programa: usuario.programa || 'No registrado',
                    codigo: 'No registrado'
                };
            } catch (error) {
                estudiante.nombre = 'Error al cargar los datos';
                console.error('Error leyendo el usuario:', error);
            }
        } else {
            estudiante.nombre = 'No se encontró el usuario';
        }
    });

   let eventos = [];

    $: eventosPendientes = eventos.filter(
        evento => evento.estado === 'pendiente'
    );
</script>


<svelte:head>
    <title>Mi perfil | Bienestar Universitario</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900;1000&display=swap" rel="stylesheet">
</svelte:head>

<div class="pagina-perfil">

    <header class="encabezado-perfil">
        <a href="/estudiantes/eventos" class="identidad-perfil">
            <div class="logo-contenedor">
                <img src="/LogoIUB.png" alt="Logo IUB">
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

        <nav class:abierto={menuAbierto} class="navegacion-perfil">
            <a href="/estudiantes/eventos" onclick={() => menuAbierto = false}>
                <span>▦</span>
                Eventos
            </a>

            <a href="/estudiantes/mi-qr" onclick={() => menuAbierto = false}>
                <span>▣</span>
                Mi código QR
            </a>

            <a href="/estudiantes/perfil" class="activo" onclick={() => menuAbierto = false}>
                <span>●</span>
                Mi perfil
            </a>
<button class="cerrar" onclick={() => {
    menuAbierto = false;
    mostrarConfirmacion = true;
}}>
    <span class="icono">↪</span>
    Cerrar sesión
</button>
        </nav>
    </header>

    <main class="contenido-principal">

        <section class="portada-perfil">
            <div class="portada-texto">
                <span>ESPACIO DEL ESTUDIANTE</span>
                <h1>Mi perfil</h1>
                <p>Consulta tu información personal y revisa tus actividades pendientes.</p>
            </div>

            <div class="decoracion-portada"></div>
        </section>

        <div class="contenedor-perfil">

            <section class="seccion-datos">
                <div class="titulo-seccion">
                    <span>INFORMACIÓN PERSONAL</span>
                    <h2>Mis datos</h2>
                </div>

                <article class="tarjeta-perfil">
                    <div class="perfil-principal">
                        <div class="avatar">♙</div>

                        <div>
                            <h3>{estudiante.nombre}</h3>
                            <span class="rol-estudiante">
                                <i></i> Estudiante
                            </span>
                        </div>
                    </div>

                    <div class="separador"></div>

                    <div class="datos-grid">
                        <div class="dato">
                            <div class="dato-icono">▤</div>
                            <div>
                               <small>{estudiante.tipoDocumento}</small>
           <strong>{estudiante.documento}</strong>
                            </div>
                        </div>

                        <div class="dato">
                            <div class="dato-icono">✉</div>
                            <div>
                                <small>Correo institucional</small>
                                <strong>{estudiante.correo}</strong>
                            </div>
                        </div>

                        <div class="dato">
                            <div class="dato-icono">▣</div>
                            <div>
                                <small>Programa académico</small>
                                <strong>{estudiante.programa}</strong>
                            </div>
                        </div>
                    </div>
                </article>
            </section>

            <section class="seccion-eventos">

                <div class="titulo-eventos">
                    <div>
                        <span>ACTIVIDADES REGISTRADAS</span>
                        <h2>Mis eventos pendientes</h2>
                        <p>Eventos a los que estás inscrito y todavía debes asistir.</p>
                    </div>

                    <div class="contador-eventos">
                        <strong>{eventosPendientes.length}</strong>
                        <small>PENDIENTES</small>
                    </div>
                </div>

                {#if eventosPendientes.length > 0}
                    <div class="lista-eventos">
                        {#each eventosPendientes as evento (evento.id)}
                            <article class="tarjeta-evento">

                                <div class="evento-icono">▦</div>

                                <div class="evento-informacion">
                                    <span class="evento-categoria">{evento.categoria}</span>
                                    <h3>{evento.nombre}</h3>

                                    <div class="evento-detalles">
                                        <span>▣ {evento.fecha}</span>
                                        <span>◷ {evento.hora}</span>
                                        <span>⌖ {evento.lugar}</span>
                                    </div>

                                    <a href="/estudiantes/mi-qr" class="boton-qr">
                                        <span>▦</span> Ver mi código QR
                                    </a>
                                </div>

                                <div class="evento-estado">
                                    <span>
                                        <i></i> Pendiente
                                    </span>
                                </div>

                            </article>
                        {/each}
                    </div>
                {:else}
                    <div class="sin-eventos">
                        <div class="icono-check">✓</div>
                        <h3>¡No tienes eventos pendientes!</h3>
                        <p>Cuando te inscribas a una actividad, aparecerá aquí. Si ya asististe, dejará de mostrarse en esta sección.</p>
                        <a href="/estudiantes/eventos">Ver eventos disponibles</a>
                    </div>
                {/if}

            </section>
        </div>
    </main>

    <footer class="footer-perfil">
        <div class="footer-contenido">
            <div class="footer-identidad">
                <img src="/LogoIUB.png" alt="Logo IUB" />

                <div>
                    <strong>BIENESTAR UNIVERSITARIO</strong>
                    <p>Institución Universitaria de Barranquilla</p>
                </div>
            </div>

            <span>© 2026 - Todos los derechos reservados</span>
        </div>
    </footer>
{#if mostrarConfirmacion}
    <div class="modal-fondo">
        <div class="modal-confirmacion">
            <div class="modal-icono">↪</div>

            <h2>¿Deseas cerrar sesión?</h2>

            <p>
                Tu sesión se cerrará y tendrás que iniciar sesión nuevamente
                para acceder al sistema.
            </p>

            <div class="modal-botones">
                <button class="boton-cancelar" onclick={cancelarCierre}>
                    Cancelar
                </button>

                <button class="boton-confirmar" onclick={cerrarSesion}>
                    Cerrar sesión
                </button>
            </div>
        </div>
    </div>
{/if}
</div>

<style>
    .pagina-perfil {
        width: 100%;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        background: #f4f6fb;
        color: #172344;
        font-family: 'Nunito', sans-serif;
        overflow-x: hidden;
    }

    .pagina-perfil * {
        box-sizing: border-box;
    }

    .pagina-perfil a {
        text-decoration: none;
    }

    /* NAVBAR */

    .encabezado-perfil {
        width: 100%;
        min-height: 88px;
        flex-shrink: 0;
        background: #142044;
        padding: 12px 7%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 25px;
        position: relative;
        z-index: 20;
    }

    .identidad-perfil {
        display: flex;
        align-items: center;
        gap: 13px;
        flex-shrink: 0;
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

    .identidad-perfil img {
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

    .navegacion-perfil {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 35px;
    }

    .navegacion-perfil a {
        position: relative;
        color: #e2e7f4;
        font-size: 16px;
        font-weight: 900;
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 8px 0 10px;
        transition: color .3s ease;
    }

    /* SUBRAYADO ANIMADO */

    .navegacion-perfil a::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 3px;
        background: #f5ca24;
        border-radius: 5px;
        transform: scaleX(0);
        transform-origin: left;
        transition: transform .3s ease;
    }

    .navegacion-perfil a:hover::after,
    .navegacion-perfil a.activo::after {
        transform: scaleX(1);
    }

    .navegacion-perfil a:hover,
    .navegacion-perfil a.activo {
        color: #f5ca24;
    }

    .navegacion-perfil a span {
        font-size: 20px;
    }

    .boton-menu {
        display: none;
    }

    /* CONTENIDO */

    .contenido-principal {
        width: 100%;
        flex: 1;
        display: block;
    }

    .portada-perfil {
        width: 92%;
        min-height: 225px;
        margin: 28px auto 0;
        padding: 45px 8%;
        background: linear-gradient(110deg, #111c3b, #174b83, #0787b5);
        border-radius: 23px;
        display: flex;
        align-items: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px rgba(20, 32, 68, .12);
    }

    .portada-texto {
        position: relative;
        z-index: 1;
    }

    .portada-texto > span {
        color: #f5ca24;
        font-size: 11px;
        font-weight: 1000;
        letter-spacing: 1.7px;
    }

    .portada-texto h1 {
        margin: 8px 0;
        color: white;
        font-size: 40px;
        font-weight: 1000;
    }

    .portada-texto p {
        color: #e0eafa;
        font-size: 15px;
        font-weight: 600;
        margin: 0;
    }

    .decoracion-portada {
        position: absolute;
        width: 300px;
        height: 300px;
        border: 35px solid #ffffff10;
        border-radius: 50%;
        right: 10%;
        top: -100px;
    }

    .contenedor-perfil {
        width: 86%;
        max-width: 1180px;
        margin: 45px auto 75px;
    }

    /* DATOS PERSONALES */

    .titulo-seccion {
        margin-bottom: 17px;
    }

    .titulo-seccion > span,
    .titulo-eventos > div:first-child > span {
        color: #0785b6;
        font-size: 11px;
        font-weight: 1000;
        letter-spacing: 1.7px;
    }

    .titulo-seccion h2,
    .titulo-eventos h2 {
        color: #172344;
        font-size: 26px;
        font-weight: 1000;
        margin: 5px 0;
    }

    .tarjeta-perfil {
        width: 100%;
        background: white;
        border: 1px solid #e9edf5;
        border-radius: 18px;
        padding: 27px 30px;
        box-shadow: 0 5px 22px #17234408;
    }

    .perfil-principal {
        display: flex;
        align-items: center;
        gap: 17px;
    }

    .avatar {
        width: 66px;
        height: 66px;
        flex-shrink: 0;
        background: #e8f5fc;
        border-radius: 17px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #0785b6;
        font-size: 35px;
        transition: transform .3s ease;
    }

    .avatar:hover {
        transform: rotate(-8deg) scale(1.08);
    }

    .perfil-principal h3 {
        font-size: 20px;
        font-weight: 1000;
        margin: 0 0 5px;
    }

    .rol-estudiante {
        color: #7b8499;
        font-size: 12px;
        font-weight: 800;
    }

    .rol-estudiante i {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #20b77a;
        border-radius: 50%;
        margin-right: 5px;
    }

    .separador {
        height: 1px;
        width: 100%;
        background: #edf0f6;
        margin: 24px 0;
    }

    .datos-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px 35px;
    }

    .dato {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }

    .dato-icono {
        width: 42px;
        height: 42px;
        flex-shrink: 0;
        background: #eff7fc;
        border-radius: 12px;
        color: #0785b6;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 19px;
        transition: transform .3s ease, background .3s ease;
    }

    .dato:hover .dato-icono {
        transform: scale(1.1) rotate(-5deg);
        background: #d8f0fc;
    }

    .dato div:last-child {
        display: flex;
        flex-direction: column;
        gap: 3px;
        min-width: 0;
    }

    .dato small {
        font-size: 11px;
        color: #8992a5;
        font-weight: 800;
    }

    .dato strong {
        font-size: 13px;
        color: #273553;
        font-weight: 900;
        overflow-wrap: anywhere;
    }

    /* EVENTOS */

    .seccion-eventos {
        width: 100%;
        margin-top: 58px;
    }

    .titulo-eventos {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        margin-bottom: 22px;
    }

    .titulo-eventos p {
        margin: 4px 0 0;
        color: #8490a4;
        font-size: 13px;
        font-weight: 700;
    }

    .contador-eventos {
        width: 92px;
        height: 76px;
        flex-shrink: 0;
        background: #e4f3fb;
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #087eaa;
        transition: transform .3s ease;
    }

    .contador-eventos:hover {
        transform: scale(1.07);
    }

    .contador-eventos strong {
        font-size: 25px;
        font-weight: 1000;
        line-height: 1;
    }

    .contador-eventos small {
        font-size: 9px;
        font-weight: 1000;
        letter-spacing: 1px;
        margin-top: 5px;
    }

    .lista-eventos {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 14px;
    }

    .tarjeta-evento {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 20px 23px;
        background: white;
        border: 1px solid #e9edf5;
        border-radius: 17px;
        box-shadow: 0 5px 20px #17234407;
        transition: transform .3s ease, box-shadow .3s ease;
    }

    .tarjeta-evento:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(20, 32, 68, .10);
    }

    .evento-icono {
        width: 54px;
        height: 54px;
        flex-shrink: 0;
        background: #eaf6fc;
        color: #0785b6;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 15px;
        font-size: 25px;
        transition: transform .3s ease, background .3s ease;
    }

    .tarjeta-evento:hover .evento-icono {
        transform: scale(1.1) rotate(-5deg);
        background: #d8f0fc;
    }

    .evento-informacion {
        flex: 1;
        min-width: 0;
    }

    .evento-categoria {
        color: #0785b6;
        font-size: 10px;
        font-weight: 1000;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .evento-informacion h3 {
        margin: 3px 0 9px;
        font-size: 18px;
        font-weight: 1000;
    }

    .evento-detalles {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 17px;
    }

    .evento-detalles span {
        font-size: 11px;
        color: #818da2;
        font-weight: 700;
    }

    .evento-estado {
        flex-shrink: 0;
    }

    .evento-estado span {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 9px 13px;
        border-radius: 20px;
        background: #fff5df;
        color: #a97508;
        font-size: 11px;
        font-weight: 1000;
        white-space: nowrap;
    }

    .evento-estado i {
        width: 7px;
        height: 7px;
        background: #e9a919;
        border-radius: 50%;
    }

    .boton-qr {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        padding: 13px;
        margin-top: 18px;
        background: #0785b6;
        color: white;
        border-radius: 12px;
        font-weight: 900;
        transition: all .3s ease;
    }

    .boton-qr:hover {
        background: #056b91;
        transform: translateY(-3px);
        box-shadow: 0 8px 18px rgba(7, 133, 182, .2);
    }

    /* SIN EVENTOS */

    .sin-eventos {
        width: 100%;
        background: white;
        border: 1px solid #e9edf5;
        border-radius: 18px;
        padding: 45px 20px;
        text-align: center;
        animation: entrarAbajo .8s ease both;
    }

    .icono-check {
        width: 58px;
        height: 58px;
        background: #e5f7ef;
        color: #20a66b;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 27px;
        font-weight: 1000;
        margin: 0 auto 14px;
    }

    .sin-eventos h3 {
        margin: 0 0 7px;
        font-size: 20px;
        font-weight: 1000;
    }

    .sin-eventos p {
        max-width: 470px;
        margin: 0 auto 18px;
        color: #8490a4;
        font-size: 13px;
        line-height: 1.6;
        font-weight: 600;
    }

    .sin-eventos a {
        display: inline-block;
        background: #087eaa;
        color: white;
        border-radius: 25px;
        padding: 11px 20px;
        font-size: 12px;
        font-weight: 900;
        transition: all .3s ease;
    }

    .sin-eventos a:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 18px rgba(7, 133, 182, .2);
    }

    /* FOOTER */

    .footer-perfil {
        width: 100%;
        flex-shrink: 0;
        background: #111c3b;
        padding: 25px 7%;
        color: white;
        animation: entrarAbajo .8s ease both;
    }

    .footer-contenido {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
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

    .footer-contenido strong {
        font-size: 12px;
        font-weight: 1000;
    }

    .footer-contenido p,
    .footer-contenido > span {
        color: #aebbd4;
        font-size: 11px;
        font-weight: 600;
        margin: 5px 0 0;
    }

    /* RESPONSIVE */

    @media (max-width: 800px) {
        .contenedor-perfil {
            width: 90%;
        }

        .tarjeta-evento {
            flex-wrap: wrap;
        }

        .evento-estado {
            width: 100%;
        }

        .evento-estado span {
            width: fit-content;
        }
    }

    @media (max-width: 700px) {
        .encabezado-perfil {
            min-height: 75px;
            padding: 10px 5%;
            gap: 10px;
            flex-wrap: wrap;
        }

        .logo-contenedor {
            width: 45px;
            height: 45px;
        }

        .identidad-perfil {
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

.navegacion-perfil {
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

.navegacion-perfil.abierto {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: translateY(0);
}



        .navegacion-perfil a {
            width: 100%;
            padding: 13px 10px;
            font-size: 14px;
            gap: 12px;
            border-radius: 8px;
        }
.navegacion-perfil a::after {
    display: none;
}

.navegacion-perfil a:hover,
.navegacion-perfil a.activo {
    background: rgba(245, 202, 36, .10);
    color: #f5ca24;
    border-radius: 8px;
}

        .navegacion-perfil a span {
            font-size: 19px;
        }

        .portada-perfil {
            width: 94%;
            min-height: 210px;
            margin: 18px auto 0;
            padding: 35px 6%;
            border-radius: 18px;
        }

        .portada-texto h1 {
            font-size: 33px;
        }

        .portada-texto p {
            font-size: 13px;
            line-height: 1.6;
        }

        .contenedor-perfil {
            margin-top: 32px;
        }

        .tarjeta-perfil {
            padding: 22px 18px;
        }

        .datos-grid {
            grid-template-columns: 1fr;
            gap: 18px;
        }

        .titulo-eventos {
            align-items: flex-start;
        }

        .titulo-eventos h2 {
            font-size: 22px;
        }

        .titulo-eventos p {
            max-width: 230px;
            line-height: 1.5;
        }

        .contador-eventos {
            width: 72px;
            height: 65px;
        }

        .tarjeta-evento {
            padding: 17px;
            gap: 12px;
        }

        .evento-informacion h3 {
            font-size: 16px;
        }

        .evento-detalles {
            flex-direction: column;
            gap: 6px;
        }

        .footer-contenido {
            flex-direction: column;
            align-items: flex-start;
        }
    }
.cerrar {
    padding: 13px 10px;
    border-radius: 8px;
}

.cerrar:hover {
    background: rgba(255,255,255,.08);
    opacity: 1;
}

    /* ANIMACIONES */

    .encabezado-perfil {
        animation: entrarArriba .7s ease both;
    }

    .portada-perfil {
        animation: entrarAbajo .8s ease both;
    }

    .portada-perfil .decoracion-portada {
        animation: flotarPerfil 6s ease-in-out infinite;
    }

    .tarjeta-perfil {
        animation: entrarAbajo .8s ease both;
        transition: transform .3s ease, box-shadow .3s ease;
    }

    .tarjeta-perfil:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(20, 32, 68, .10);
    }

    .tarjeta-evento {
        animation: entrarAbajo .8s ease both;
    }

    @keyframes entrarArriba {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes entrarAbajo {
        from {
            opacity: 0;
            transform: translateY(22px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes flotarPerfil {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(16px);
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
.cerrar {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    padding: 12px 15px;
    background: transparent;
    border: none;
    color: white;
    font-family: inherit;
    font-size: inherit;
    text-align: left;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.cerrar::after {
    content: '';
    position: absolute;
    left: 15px;
    bottom: 5px;
    width: 0;
    height: 2px;
    background: #0785b6;
    transition: width 0.3s ease;
}

.cerrar:hover::after {
    width: calc(100% - 30px);
}

.cerrar:hover {
    opacity: 0.8;
}

.modal-fondo {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 20, 45, 0.65);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    z-index: 9999;
}

.modal-confirmacion {
    width: 100%;
    max-width: 400px;
    background: white;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    animation: aparecerModal 0.25s ease;
}

.modal-icono {
    width: 55px;
    height: 55px;
    margin: 0 auto 15px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: #e7f5fc;
    color: #0785b6;
    font-size: 28px;
}

.modal-confirmacion h2 {
    color: #18233f;
    font-size: 21px;
    font-weight: 1000;
    margin: 10px 0;
}

.modal-confirmacion p {
    color: #8995a9;
    font-size: 13px;
    line-height: 1.6;
}

.modal-botones {
    display: flex;
    gap: 12px;
    margin-top: 25px;
}

.modal-botones button {
    flex: 1;
    padding: 13px 10px;
    border: none;
    border-radius: 10px;
    font-family: inherit;
    font-size: 12px;
    font-weight: 900;
    cursor: pointer;
    transition: 0.2s;
}

.boton-cancelar {
    background: #edf1f7;
    color: #596781;
}

.boton-cancelar:hover {
    background: #dfe5ef;
}

.boton-confirmar {
    background: #0785b6;
    color: white;
}

.boton-confirmar:hover {
    background: #056b91;
}

@keyframes aparecerModal {
    from {
        opacity: 0;
        transform: translateY(10px) scale(0.97);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}
</style>
