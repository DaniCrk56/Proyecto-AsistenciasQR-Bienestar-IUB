
<script>
    import { onMount } from 'svelte';
    import { Html5Qrcode } from 'html5-qrcode';

    let idEvento = '';
    let lector;
    let mostrarMensaje = false;
    let procesando = false;

    let tituloMensaje = '';
    let textoMensaje = '';
    let tipoMensaje = 'exito';
    let estadoCamara = 'Iniciando cámara...';

    const API_URL = 'https://proyecto-asistenciasqr-bienestar-iub.onrender.com';

    onMount(() => {

        let componenteActivo = true;

        const parametros = new URLSearchParams(window.location.search);
        idEvento = parametros.get('id_evento') || '';

        async function iniciarCamara() {

            if (!idEvento) {
                estadoCamara = 'No se recibió el evento seleccionado';
                return;
            }

            const token = localStorage.getItem('token');

            if (!token) {
                estadoCamara = 'Debes iniciar sesión nuevamente';
                return;
            }

            lector = new Html5Qrcode('lector-qr');

            try {
                await lector.start(
                    { facingMode: 'environment' },
                    {
                        fps: 10,
                        qrbox: {
                            width: 220,
                            height: 220
                        }
                    },
                    codigoQR => {
                        registrarAsistencia(codigoQR);
                    },
                    () => {}
                );

                if (!componenteActivo) {
                    await lector.stop();
                    lector.clear();
                    return;
                }

                estadoCamara = 'Cámara activa. Esperando código QR';

            } catch (error) {
                console.error('Error al iniciar la cámara:', error);

                if (componenteActivo) {
                    estadoCamara = 'No se pudo activar la cámara. Verifica los permisos.';
                }
            }
        }

        iniciarCamara();

        // Apagar la cámara cuando se abandona la página
        return () => {

            componenteActivo = false;

            if (lector && lector.isScanning) {
                lector.stop()
                    .then(() => {
                        lector.clear();
                    })
                    .catch(error => {
                        console.error('Error al apagar la cámara:', error);
                    });
            }
        };
    });

    async function registrarAsistencia(codigoQR) {

        if (procesando) {
            return;
        }

        procesando = true;

        if (lector && lector.isScanning) {
            lector.pause(true);
        }

        try {
            const token = localStorage.getItem('token');

            const respuesta = await fetch(`${API_URL}/asistencias/escanear`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    codigo_qr: codigoQR,
                    id_evento: Number(idEvento)
                })
            });

            const datos = await respuesta.json();

            if (respuesta.ok) {
                tipoMensaje = 'exito';
                tituloMensaje = '¡Asistencia registrada!';
                textoMensaje = datos.mensaje || 'La asistencia se registró exitosamente.';

            } else if (respuesta.status === 409) {
                tipoMensaje = 'advertencia';
                tituloMensaje = 'Asistencia duplicada';
                textoMensaje = datos.detail || 'Este estudiante ya tiene asistencia registrada.';

            } else if (respuesta.status === 404) {
                tipoMensaje = 'error';
                tituloMensaje = 'QR no válido';
                textoMensaje = datos.detail || 'El QR no pertenece a este evento.';

            } else {
                tipoMensaje = 'error';
                tituloMensaje = 'No se pudo registrar';
                textoMensaje = datos.detail || 'Ocurrió un error al validar el código QR.';
            }

        } catch (error) {
            console.error('Error al registrar asistencia:', error);

            tipoMensaje = 'error';
            tituloMensaje = 'Error de conexión';
            textoMensaje = 'No fue posible comunicarse con el servidor.';
        }

        mostrarMensaje = true;

        setTimeout(() => {

            mostrarMensaje = false;
            procesando = false;

            if (lector && lector.isScanning) {
                lector.resume();
                estadoCamara = 'Cámara activa. Esperando código QR';
            }

        }, 3000);
    }
</script>



<svelte:head>
    <title>Escáner QR | Bienestar Universitario</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900;1000&display=swap" rel="stylesheet">
</svelte:head>

<div class="pagina">

    <header class="encabezado">
        <a href="/admin/admin" class="volver">
            <span>←</span> Volver al panel
        </a>

        <div class="marca">
            <img src="/LogoIUB.png" alt="Logo IUB">
            <div>
                <strong>BIENESTAR</strong>
                <span>UNIVERSITARIO</span>
            </div>
        </div>
        
    </header>

    <main class="contenido">

        <div class="titulo">
            <span class="etiqueta">CONTROL DE ASISTENCIA</span>
            <h1>Escáner de códigos QR</h1>
            <p>Ubica el código QR del estudiante dentro del área de escaneo.</p>
        </div>

        <section class="scanner-contenedor">

            <div class="scanner-superior">
                <div>
                    <h2>Área de escaneo</h2>
                    <p>Escanea el código QR del estudiante</p>
                </div>

                <div class="esperando">
                    <span></span>
                    Esperando código QR
                </div>
            </div>

            <div class="camara">

              <div class="fondo-camara">
    <div class="icono-camara">▣</div>

    <h3>Escáner de estudiantes</h3>

    <p>{estadoCamara}</p>

    <div class="marco">
        <span class="esquina arriba-izquierda"></span>
        <span class="esquina arriba-derecha"></span>
        <span class="esquina abajo-izquierda"></span>
        <span class="esquina abajo-derecha"></span>

        <div id="lector-qr"></div>
    </div>

    <span class="texto-marco">UBICA EL CÓDIGO QR AQUÍ</span>
</div>

            </div>

            <div class="scanner-inferior">
                <div class="instruccion">
                    <span class="instruccion-icono">ⓘ</span>
                    <p>El código QR debe estar completamente visible dentro del área de escaneo.</p>
                </div>

                <div class="indicador">
                    <span></span>
                    Lector preparado
                </div>
            </div>

        </section>

        <div class="ayuda">
            <span>✦</span>
            <p>Una vez conectado el lector, la asistencia se registrará automáticamente al validar el código QR.</p>
        </div>

    </main>

  {#if mostrarMensaje}
    <div class="fondo-notificacion">
        <div class="notificacion">
            <div class="check"
                class:advertencia={tipoMensaje === 'advertencia'}
                class:error={tipoMensaje === 'error'}>
                {tipoMensaje === 'exito' ? '✓' : '!'}
            </div>

            <h2>{tituloMensaje}</h2>
            <p>{textoMensaje}</p>
        </div>
    </div>
{/if}

</div>

<style>
    :global(*) {
        box-sizing: border-box;
    }

    :global(body) {
        margin: 0;
        background: #f3f6fc;
        font-family: 'Nunito', sans-serif;
    }

    .pagina {
        min-height: 100vh;
        color: #172442;
    }

    .encabezado {
        width: 100%;
        min-height: 82px;
        background: #111c3b;
        padding: 15px 5%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
    }

    .volver {
        color: #d5dfef;
        text-decoration: none;
        font-size: 13px;
        font-weight: 800;
    }

    .volver span {
        font-size: 20px;
        margin-right: 7px;
    }

    .marca {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .marca img {
        width: 43px;
        height: 43px;
        object-fit: contain;
        background: white;
        border-radius: 10px;
        padding: 3px;
    }

    .marca strong,
    .marca span {
        display: block;
    }

    .marca strong {
        font-size: 14px;
        font-weight: 1000;
    }

    .marca span {
        font-size: 9px;
        letter-spacing: 2px;
        color: #aab8d0;
        font-weight: 900;
    }

  

    .estado span,
    .esperando span,
    .indicador span {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #20cf8b;
        border-radius: 50%;
        margin-right: 7px;
    }

    .contenido {
        max-width: 1050px;
        margin: auto;
        padding: 40px 25px;
    }

    .titulo {
        text-align: center;
        margin-bottom: 30px;
    }

    .etiqueta {
        font-size: 10px;
        color: #0785b6;
        font-weight: 1000;
        letter-spacing: 2px;
    }

    .titulo h1 {
        font-size: 32px;
        font-weight: 1000;
        margin: 7px 0;
    }

    .titulo p {
        color: #8290a8;
        font-size: 13px;
    }

    .evento {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        display: flex;
        align-items: center;
        gap: 17px;
        box-shadow: 0 5px 20px #15264a08;
        margin-bottom: 25px;
    }

    .evento-icono {
        width: 53px;
        height: 53px;
        border-radius: 14px;
        background: #e5f4fc;
        display: grid;
        place-items: center;
        color: #0785b6;
        font-size: 27px;
    }

    .evento-info {
        flex: 1;
    }

    .evento-info > span,
    .evento-id span {
        color: #0785b6;
        font-size: 9px;
        font-weight: 1000;
        letter-spacing: 1px;
    }

    .evento-info h2 {
        font-size: 17px;
        font-weight: 1000;
        margin: 3px 0;
    }

    .evento-info p {
        color: #8793a8;
        font-size: 11px;
        margin: 0;
    }

    .evento-id {
        text-align: right;
    }

    .evento-id strong {
        display: block;
        font-size: 14px;
        margin-top: 5px;
    }

    .scanner-contenedor {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 6px 25px #15264a0a;
    }

    .scanner-superior {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 20px;
    }

    .scanner-superior h2 {
        font-size: 19px;
        font-weight: 1000;
        margin: 0;
    }

    .scanner-superior p {
        color: #929db1;
        font-size: 11px;
        margin: 4px 0 0;
    }

    .esperando {
        background: #e9f8f1;
        color: #159a65;
        border-radius: 20px;
        padding: 9px 13px;
        font-size: 10px;
        font-weight: 900;
    }

    .camara {
        background: #111c3b;
        border-radius: 15px;
        padding: 30px;
        min-height: 390px;
        display: grid;
        place-items: center;
        overflow: hidden;
    }

    .fondo-camara {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        color: white;
    }

    .icono-camara {
        width: 45px;
        height: 45px;
        border-radius: 13px;
        background: #243658;
        display: grid;
        place-items: center;
        font-size: 23px;
        color: #91c9e5;
    }

    .fondo-camara h3 {
        font-size: 17px;
        margin: 10px 0 3px;
        font-weight: 1000;
    }

    .fondo-camara > p {
        font-size: 11px;
        color: #aab8d0;
        margin: 0 0 20px;
    }

    .marco {
        position: relative;
        width: 190px;
        height: 190px;
        border: 1px solid #42617e;
        border-radius: 12px;
        display: grid;
        place-items: center;
    }

    .esquina {
        position: absolute;
        width: 28px;
        height: 28px;
        border-color: #19b9ef;
        border-style: solid;
    }

    .arriba-izquierda {
        top: -2px;
        left: -2px;
        border-width: 4px 0 0 4px;
        border-radius: 9px 0 0 0;
    }

    .arriba-derecha {
        top: -2px;
        right: -2px;
        border-width: 4px 4px 0 0;
        border-radius: 0 9px 0 0;
    }

    .abajo-izquierda {
        bottom: -2px;
        left: -2px;
        border-width: 0 0 4px 4px;
        border-radius: 0 0 0 9px;
    }

    .abajo-derecha {
        bottom: -2px;
        right: -2px;
        border-width: 0 4px 4px 0;
        border-radius: 0 0 9px 0;
    }

    .linea-escaneo {
        position: absolute;
        left: 10px;
        right: 10px;
        height: 2px;
        background: #19b9ef;
        box-shadow: 0 0 12px #19b9ef;
        animation: movimiento 3s ease-in-out infinite alternate;
    }

    @keyframes movimiento {
        from { top: 15px; }
        to { top: 170px; }
    }

    .texto-marco {
        position: absolute;
        bottom: -30px;
        color: #9eb3cc;
        font-size: 8px;
        font-weight: 900;
        letter-spacing: 1.5px;
        white-space: nowrap;
    }

    .scanner-inferior {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px;
        margin-top: 25px;
    }

    .instruccion {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .instruccion-icono {
        color: #0785b6;
        font-size: 20px;
    }

    .instruccion p {
        color: #8a96aa;
        font-size: 10px;
    }

    .indicador {
        color: #159a65;
        font-size: 10px;
        font-weight: 900;
        white-space: nowrap;
    }

    .ayuda {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #e7f5fc;
        padding: 14px 18px;
        border-radius: 12px;
        margin-top: 20px;
    }

    .ayuda span {
        color: #0785b6;
        font-size: 22px;
    }

    .ayuda p {
        color: #54738b;
        font-size: 11px;
        margin: 0;
    }

    .fondo-notificacion {
        position: fixed;
        inset: 0;
        z-index: 10;
        background: #101c3b77;
        display: grid;
        place-items: center;
        padding: 20px;
        animation: aparecer 0.2s ease;
    }

    .notificacion {
        background: white;
        border-radius: 22px;
        padding: 35px 45px;
        text-align: center;
        width: 100%;
        max-width: 380px;
        box-shadow: 0 20px 60px #0003;
        animation: subir 0.3s ease;
    }

    .check {
        width: 65px;
        height: 65px;
        margin: auto;
        display: grid;
        place-items: center;
        background: #e1f8eb;
        color: #16a36c;
        border-radius: 50%;
        font-size: 35px;
        font-weight: 1000;
    }

    .notificacion h2 {
        color: #172442;
        font-size: 20px;
        font-weight: 1000;
        margin: 15px 0 5px;
    }

    .notificacion p {
        color: #8793a8;
        font-size: 12px;
    }

    @keyframes aparecer {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes subir {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 650px) {
        .encabezado {
            padding: 15px;
            flex-wrap: wrap;
            gap: 12px;
        }

        .marca {
            order: -1;
            width: 100%;
            justify-content: center;
        }
.cerrar {
    margin-left: auto;
}

        .contenido {
            padding: 28px 15px;
        }

        .titulo h1 {
            font-size: 25px;
        }

        .evento {
            flex-wrap: wrap;
        }

        .evento-info {
            min-width: 180px;
        }

        .evento-id {
            width: 100%;
            text-align: left;
        }

        .scanner-contenedor {
            padding: 17px;
        }

        .scanner-superior,
        .scanner-inferior {
            align-items: flex-start;
            flex-direction: column;
        }

        .camara {
            padding: 25px 12px;
            min-height: 350px;
        }
    }

.marco {
    width: 260px;
    height: 260px;
    padding: 10px;
    overflow: hidden;
}

#lector-qr {
    width: 100%;
    max-width: 240px;
    overflow: hidden;
    border-radius: 10px;
}

:global(#lector-qr video) {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover;
    border-radius: 10px;
}

.texto-marco {
    position: static;
    margin-top: 12px;
}

.check.advertencia {
    background: #fff3cd;
    color: #b78103;
}

.check.error {
    background: #fde8e8;
    color: #d93636;
}

</style>
