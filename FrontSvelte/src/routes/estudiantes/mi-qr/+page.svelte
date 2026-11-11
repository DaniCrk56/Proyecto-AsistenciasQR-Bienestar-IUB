
<script>
    import { onMount } from 'svelte';
    import QRCode from 'qrcode';

    let estudiante = {
        nombre: 'Cargando...',
        documento: 'No registrado',
        programa: 'No registrado',
        codigo: 'No registrado'
    };

    let qrImagen = '';
    let mensaje = '';
    let menuAbierto = false;

    onMount(async () => {
        const usuarioGuardado = localStorage.getItem('usuario');

        if (usuarioGuardado) {
            try {
                const usuario = JSON.parse(usuarioGuardado);

                estudiante = {
                    nombre: `${usuario.nombres || ''} ${usuario.apellidos || ''}`.trim(),
                    documento: usuario.numero_documento || 'No registrado',
                    programa: usuario.programa || 'No registrado',
                    codigo: usuario.id ? `IUB-EST-${usuario.id}` : 'No registrado'
                };

                if (usuario.id) {
                    const contenidoQR = JSON.stringify({
                        tipo: 'estudiante',
                        id: usuario.id
                    });

                    qrImagen = await QRCode.toDataURL(contenidoQR, {
                        width: 400,
                        margin: 2,
                        errorCorrectionLevel: 'H',
                        color: {
                            dark: '#142044',
                            light: '#FFFFFF'
                        }
                    });
                } else {
                    mensaje = 'No se encontró el identificador del estudiante.';
                }

            } catch (error) {
                console.error('Error generando el QR:', error);
                mensaje = 'No fue posible generar el código QR.';
            }
        } else {
            estudiante.nombre = 'No se encontró el usuario';
            mensaje = 'Inicia sesión para consultar tu código QR.';
        }
    });

    function descargarQR() {
        if (!qrImagen) {
            mensaje = 'El código QR todavía no está disponible.';
            return;
        }

        const enlace = document.createElement('a');
        enlace.href = qrImagen;
        enlace.download = `QR-${estudiante.codigo}.png`;
        enlace.click();

        mensaje = 'Tu código QR se descargó correctamente.';
    }
</script>


<svelte:head>
    <title>Mi código QR | Bienestar Universitario IUB</title>
    <meta name="description" content="Consulta tu código QR personal para registrar tu asistencia a los eventos universitarios." />
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

        <section class="presentacion">
            <div class="presentacion-contenido">
                <span class="etiqueta">
                    <span></span>
                    IDENTIFICACIÓN UNIVERSITARIA
                </span>

                <h1>Mi código <span>QR.</span></h1>

                <p>
                    Tu identificación digital para participar y registrar
                    tu asistencia en las actividades de Bienestar Universitario.
                </p>
            </div>

            <div class="presentacion-decoracion">
                <div class="circulo circulo-1"></div>
                <div class="circulo circulo-2"></div>
                <span>QR</span>
            </div>
        </section>

        <section class="contenido">

            <div class="titulo-seccion">
                <div>
                    <span class="subtitulo">TU IDENTIFICACIÓN PERSONAL</span>
                    <h2>Mi identificación digital</h2>
                    <p>Presenta este código al personal encargado para registrar tu asistencia.</p>
                </div>

                <div class="estado">
                    <span></span>
                    Código de demostración
                </div>
            </div>

            <div class="qr-layout">

                <div class="tarjeta-qr">

                    <div class="qr-cabecera">
                        <div class="qr-logo">
                            <img src="/LogoIUB.png" alt="Logo institucional" />
                        </div>

                        <div>
                            <strong>INSTITUCIÓN UNIVERSITARIA</strong>
                            <span>DE BARRANQUILLA</span>
                        </div>
                    </div>

                    <div class="linea"></div>

                    <div class="qr-titulo">
                        <span>IDENTIFICACIÓN DE ESTUDIANTE</span>
                        <h3>Código personal</h3>
                    </div>

                  <div class="qr-demo">
    {#if qrImagen}
        <img
            src={qrImagen}
            alt="Código QR personal del estudiante"
            class="qr-imagen"
        />
    {:else}
        <div class="qr-cargando">
            Generando QR...
        </div>
    {/if}
</div>

                    <div class="codigo">
                        <span>CÓDIGO DE IDENTIFICACIÓN</span>
                        <strong>{estudiante.codigo}</strong>
                    </div>

                    <div class="qr-pie">
                        <span>BIENESTAR UNIVERSITARIO</span>
                        <span>IUB · 2026</span>
                    </div>

                </div>

            </div>

            <section class="instrucciones">
                <div class="instrucciones-titulo">
                    <span class="subtitulo">FÁCIL Y RÁPIDO</span>
                    <h2>¿Cómo utilizar tu código QR?</h2>
                </div>

                <div class="pasos">

                    <div class="paso">
                        <div class="paso-numero">01</div>
                        <div class="paso-icono">▣</div>
                        <h3>Consulta tu QR</h3>
                        <p>Ingresa a este apartado desde tu cuenta estudiantil.</p>
                    </div>

                    <div class="paso">
                        <div class="paso-numero">02</div>
                        <div class="paso-icono">▤</div>
                        <h3>Presenta tu código</h3>
                        <p>Muestra tu identificación digital al ingresar al evento.</p>
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

    /* ENCABEZADO: MISMO DISEÑO QUE EVENTOS */

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
    }

    .enlace span {
        font-size: 20px;
    }

    .enlace:hover,
    .enlace.activo {
        color: #f5ca24;
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
    }

    .circulo-2 {
        width: 175px;
        height: 175px;
        border-color: rgba(245,202,36,.5);
    }

    .presentacion-decoracion > span {
        color: white;
        font-size: 55px;
        font-weight: 1000;
        transform: rotate(-10deg);
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
    }

    .estado span {
        width: 7px;
        height: 7px;
        background: #d5a900;
        border-radius: 50%;
    }

    /* DISTRIBUCIÓN QR */

    .qr-layout {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

    .tarjeta-qr {
    width: 100%;
    max-width: 430px;
    margin: 0 auto;
    background: white;
    border: 1px solid #e9edf4;
    border-radius: 22px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(20,32,68,.06);
    text-align: center;
}

    .qr-cabecera {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }

    .qr-logo {
        width: 52px;
        height: 52px;
        padding: 4px;
        border-radius: 10px;
        background: #fff;
    }

    .qr-logo img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .qr-cabecera div:last-child {
        display: flex;
        flex-direction: column;
        text-align: left;
        gap: 4px;
    }

    .qr-cabecera strong {
        color: #142044;
        font-size: 11px;
        font-weight: 1000;
    }

    .qr-cabecera span {
        color: #b18c0b;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1px;
    }

    .linea {
        height: 1px;
        background: #edf0f5;
        margin: 22px 0;
    }

    .qr-titulo span {
        color: #929bad;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1.5px;
    }

    .qr-titulo h3 {
        color: #142044;
        font-size: 20px;
        font-weight: 1000;
        margin: 6px 0 20px;
    }

    .qr-contenedor {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .qr-demo {
    width: 230px;
    height: 230px;
    padding: 12px;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    border: 1px solid #e5eaf2;
    border-radius: 12px;
    box-shadow: 0 5px 18px rgba(20,32,68,.06);
    animation: aparecerCodigo .9s ease both;
    animation-delay: .3s;
    transition: box-shadow .3s ease;
}

    .qr-patron {
        display: grid;
        width: 100%;
        height: 100%;
        grid-template-columns: repeat(21, 1fr);
        grid-template-rows: repeat(21, 1fr);
        gap: 2px;
    }

    .qr-patron span {
        background: white;
        border-radius: 1px;
    }

    .qr-patron span.activo {
        background: #142044;
    }

    .codigo {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-top: 20px;
    }

    .codigo span {
        color: #8992a5;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1px;
    }

    .codigo strong {
        color: #142044;
        font-size: 17px;
        font-weight: 1000;
        letter-spacing: 1px;
    }

    .qr-pie {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #edf0f5;
        padding-top: 15px;
        margin-top: 22px;
        color: #929bad;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: .5px;
    }

    .informacion {
        background: white;
        border: 1px solid #e9edf4;
        border-radius: 22px;
        padding: 32px;
        box-shadow: 0 10px 30px rgba(20,32,68,.06);
    }

    .informacion-cabecera {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 27px;
    }

    .avatar {
        width: 49px;
        height: 49px;
        border-radius: 15px;
        display: grid;
        place-items: center;
        color: white;
        background: linear-gradient(135deg, #142044, #3476bc);
        font-size: 21px;
        font-weight: 1000;
    }

    .informacion-cabecera span {
        color: #b18c0b;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1.5px;
    }

    .informacion-cabecera h3 {
        color: #142044;
        font-size: 21px;
        font-weight: 1000;
        margin: 4px 0 0;
    }

    .campo {
        display: flex;
        flex-direction: column;
        gap: 7px;
        padding: 15px 0;
        border-bottom: 1px solid #edf0f5;
    }

    .campo span {
        color: #8992a5;
        font-size: 10px;
        font-weight: 700;
    }

    .campo strong {
        color: #263452;
        font-size: 13px;
        font-weight: 900;
    }

    .aviso {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 15px;
        margin-top: 22px;
        background: #edf3fb;
        border-radius: 13px;
    }

    .aviso-icono {
        color: #1d4b8c;
        font-size: 19px;
        font-weight: 1000;
    }

    .aviso p {
        color: #536580;
        font-size: 10px;
        line-height: 1.7;
        margin: 0;
    }

    .boton-descargar {
        width: 100%;
        margin-top: 22px;
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

    .boton-descargar:hover {
        background: #f5ca24;
        color: #142044;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(245,202,36,.25);
    }

    .boton-descargar span {
        font-size: 20px;
    }

    .mensaje {
        padding: 12px;
        margin-top: 14px;
        background: #edf3fb;
        border-radius: 10px;
        color: #234878;
        font-size: 11px;
        line-height: 1.6;
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

    /* RESPONSIVE */

    @media (max-width: 850px) {
        .qr-layout {
            grid-template-columns: 1fr;
        }

        .presentacion-decoracion {
            right: 2%;
            opacity: .4;
        }
    }

    /* MENÚ RESPONSIVE: IGUAL AL DE EVENTOS */

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
            display: none;
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
        }

        .navegacion.abierto {
            display: flex;
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

        .tarjeta-qr,
        .informacion {
            padding: 22px;
        }

        .qr-demo {
            width: 210px;
            height: 210px;
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
    }


.encabezado {
    animation: entradaQRArriba .7s ease both;
}

.presentacion {
    animation: entradaQRAbajo .8s ease both;
}

.circulo-1 {
    animation: flotarQR 6s ease-in-out infinite;
}

.circulo-2 {
    animation: flotarQR 5s ease-in-out infinite reverse;
}


.presentacion-decoracion > span {
    animation: girarQR 5s ease-in-out infinite;
}

.tarjeta-qr {
    animation: entradaQRAbajo .8s ease both;
    transition: transform .3s ease, box-shadow .3s ease;
    animation-delay: .1s;
}


.tarjeta-qr:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 35px rgba(20, 32, 68, .12);
}

.qr-demo {
    animation: aparecerCodigo .9s ease both;
    animation-delay: .3s;
    transition: box-shadow .3s ease;
}

.qr-demo:hover {
    box-shadow: 0 8px 25px rgba(20, 32, 68, .13);
}


.informacion {
    animation: entradaQRAbajo .8s ease both;
    animation-delay: .2s;
    transition: transform .3s ease, box-shadow .3s ease;
}

.informacion:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 35px rgba(20, 32, 68, .10);
}


.campo {
    transition: padding-left .25s ease, background .25s ease;
}

.campo:hover {
    padding-left: 8px;
}


.avatar {
    transition: transform .3s ease;
}

.avatar:hover {
    transform: rotate(-8deg) scale(1.08);
}


.boton-descargar {
    transition: transform .3s ease, box-shadow .3s ease, background .3s ease;
}


.mensaje {
    animation: entradaQRAbajo .4s ease both;
}


.paso {
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
    box-shadow: 0 15px 30px rgba(20, 32, 68, .10);
}

.paso-icono {
    transition: transform .3s ease, background .3s ease;
}

.paso:hover .paso-icono {
    transform: scale(1.12) rotate(-5deg);
    background: #dceafa;
}

footer {
    animation: entradaQRAbajo .8s ease both;
}


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

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation: none !important;
        transition: none !important;
    }
}

/* SUBRAYADO ANIMADO DEL MENÚ */

.enlace {
    position: relative;
    padding-bottom: 7px;
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
.qr-imagen {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    margin: auto;
}

.qr-cargando {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #8992a5;
    font-size: 12px;
    font-weight: 900;
    text-align: center;
}
</style>
