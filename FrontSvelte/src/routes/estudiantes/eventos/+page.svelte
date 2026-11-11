
<script>
    import { onMount } from 'svelte';
    import Swiper from 'swiper';
    import { EffectCoverflow, Navigation, Pagination } from 'swiper/modules';

    import 'swiper/css';
    import 'swiper/css/effect-coverflow';
    import 'swiper/css/navigation';
    import 'swiper/css/pagination';

    let swiper;
    let actividadSeleccionada = 0;
    let mensaje = '';
    let menuAbierto = false;

    let actividades = [
        {
            nombre: 'Jornada deportiva',
            categoria: 'Deportes',
            fecha: '20 de noviembre de 2026',
            hora: '8:00 a. m. - 10:00 a. m.',
            lugar: 'Cancha universitaria',
            descripcion: 'Participa en una jornada llena de energía, actividad física y compañerismo. Disfruta de diferentes actividades deportivas junto a la comunidad universitaria.',
            imagen: 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=900'
        },
        {
            nombre: 'Festival cultural',
            categoria: 'Cultura',
            fecha: '25 de noviembre de 2026',
            hora: '2:00 p. m. - 5:00 p. m.',
            lugar: 'Auditorio principal',
            descripcion: 'Un espacio para disfrutar del talento artístico, la música, la danza y las diferentes expresiones culturales de nuestra comunidad.',
            imagen: 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=900'
        },
        {
            nombre: 'Encuentro de bienestar',
            categoria: 'Bienestar',
            fecha: '28 de noviembre de 2026',
            hora: '9:00 a. m. - 12:00 p. m.',
            lugar: 'Bloque académico',
            descripcion: 'Un encuentro dedicado al bienestar físico y emocional, con actividades recreativas y espacios para compartir.',
            imagen: 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=900'
        },
        {
            nombre: 'Taller de liderazgo',
            categoria: 'Formación',
            fecha: '3 de diciembre de 2026',
            hora: '10:00 a. m. - 12:00 p. m.',
            lugar: 'Sala de conferencias',
            descripcion: 'Fortalece tus habilidades personales y aprende herramientas para desarrollar tu liderazgo dentro y fuera de la universidad.',
            imagen: 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=900'
        },
        {
            nombre: 'Feria universitaria',
            categoria: 'Integración',
            fecha: '10 de diciembre de 2026',
            hora: '8:00 a. m. - 1:00 p. m.',
            lugar: 'Plazoleta principal',
            descripcion: 'Comparte con estudiantes, conoce diferentes iniciativas universitarias y disfruta de una jornada de integración.',
            imagen: 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=900'
        }
    ];

    function inscribirse() {
        mensaje = 'La inscripción estará disponible cuando conectemos esta página con el sistema.';
    }

    onMount(() => {
        swiper = new Swiper('.eventos-swiper', {
            modules: [EffectCoverflow, Navigation, Pagination],

            effect: 'coverflow',
            grabCursor: true,
            centeredSlides: true,

            slidesPerView: 5,
            slidesPerGroup: 1,

            loop: true,
            loopAdditionalSlides: 5,
            speed: 650,

            coverflowEffect: {
                rotate: 0,
                stretch: 0,
                depth: 100,
                modifier: 1.2,
                slideShadows: false
            },

            navigation: {
                nextEl: '.boton-siguiente',
                prevEl: '.boton-anterior'
            },

            pagination: {
                el: '.paginacion-eventos',
                clickable: true
            },

            breakpoints: {
                0: {
                    slidesPerView: 1.15,
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 0,
                        depth: 50,
                        modifier: 1,
                        slideShadows: false
                    }
                },

                600: {
                    slidesPerView: 2.2,
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 0,
                        depth: 70,
                        modifier: 1.1,
                        slideShadows: false
                    }
                },

                900: {
                    slidesPerView: 3,
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 0,
                        depth: 80,
                        modifier: 1.1,
                        slideShadows: false
                    }
                },

                1200: {
                    slidesPerView: 5,
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 0,
                        depth: 100,
                        modifier: 1.2,
                        slideShadows: false
                    }
                }
            },

            on: {
                slideChange: function () {
                    actividadSeleccionada = this.realIndex % actividades.length;
                    mensaje = '';
                }
            }
        });

        return () => {
            if (swiper) {
                swiper.destroy(true, true);
            }
        };
    });
</script>

<svelte:head>
    <title>Eventos | Bienestar Universitario</title>
    <meta name="description" content="Conoce los eventos y actividades de Bienestar Universitario." />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
    <link
        href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900;1000&display=swap"
        rel="stylesheet"
    />
</svelte:head>

<div class="pagina">

    <!-- ENCABEZADO -->
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
                class="enlace activo"
                onclick={() => menuAbierto = false}
            >
                <span>▦</span>
                Eventos
            </a>

            <a
                href="/estudiantes/mi-qr"
                class="enlace"
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

    <!-- PRESENTACIÓN -->
    <section class="presentacion">
        <div class="presentacion-contenido">
            <span class="etiqueta">BIENESTAR UNIVERSITARIO</span>

            <h1>
                Vive la experiencia
                <span>universitaria</span>
            </h1>

            <p>
                Descubre, participa y disfruta de las actividades
                que tenemos preparadas para ti.
            </p>

            <a href="#eventos" class="boton-descubrir">
                Descubrir eventos
                <span>↓</span>
            </a>
        </div>

        <div class="presentacion-decoracion">
            <div class="circulo circulo-uno"></div>
            <div class="circulo circulo-dos"></div>
            <div class="figura-icono">✦</div>
        </div>
    </section>

    <!-- CARRUSEL DE EVENTOS -->
    <main id="eventos" class="contenido">

        <div class="titulo-seccion">
            <div class="titulo-textos">
                <span class="subtitulo">NO TE LO PIERDAS</span>
                <h2>Próximos eventos</h2>
                <p>Encuentra actividades para aprender, compartir y disfrutar.</p>
            </div>

            <div class="controles">
                <button class="boton-carrusel boton-anterior" aria-label="Evento anterior">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M15 18L9 12L15 6" />
                    </svg>
                </button>

                <button class="boton-carrusel boton-siguiente" aria-label="Evento siguiente">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M9 18L15 12L9 6" />
                    </svg>
                </button>
            </div>
        </div>

        <div class="carrusel-contenedor">
            <div class="swiper eventos-swiper">
                <div class="swiper-wrapper">
                    {#each actividades as actividad, i}
                        <div class="swiper-slide">
                            <div class="tarjeta-evento">
                                <img src={actividad.imagen} alt={actividad.nombre} />

                                <div class="capa-tarjeta">
                                    <span class="categoria">{actividad.categoria}</span>
                                    <h3>{actividad.nombre}</h3>
                                    <span class="ver-evento">Ver evento →</span>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <div class="paginacion-eventos"></div>
        </div>

        <!-- INFORMACIÓN DEL EVENTO -->
        <section class="detalle-evento">
            <div class="detalle-texto">
                <span class="subtitulo">CONOCE MÁS</span>

                <h2>{actividades[actividadSeleccionada].nombre}</h2>

                <p class="descripcion">
                    {actividades[actividadSeleccionada].descripcion}
                </p>

                <div class="informacion-evento">
                    <div class="dato-evento">
                        <span class="dato-icono">▣</span>
                        <div>
                            <small>Fecha</small>
                            <strong>{actividades[actividadSeleccionada].fecha}</strong>
                        </div>
                    </div>

                    <div class="dato-evento">
                        <span class="dato-icono">◷</span>
                        <div>
                            <small>Horario</small>
                            <strong>{actividades[actividadSeleccionada].hora}</strong>
                        </div>
                    </div>

                    <div class="dato-evento">
                        <span class="dato-icono">⌖</span>
                        <div>
                            <small>Lugar</small>
                            <strong>{actividades[actividadSeleccionada].lugar}</strong>
                        </div>
                    </div>
                </div>

                <button class="boton-inscripcion" onclick={inscribirse}>
                    Inscribirme al evento
                    <span>→</span>
                </button>

                {#if mensaje}
                    <p class="mensaje">{mensaje}</p>
                {/if}
            </div>

            <div class="detalle-imagen">
                <img
                    src={actividades[actividadSeleccionada].imagen}
                    alt={actividades[actividadSeleccionada].nombre}
                />

                <div class="detalle-etiqueta">
                    <span>BIENESTAR</span>
                    <strong>UNIVERSITARIO</strong>
                </div>
            </div>
        </section>
    </main>

    <!-- PIE DE PÁGINA -->
    <footer class="pie-pagina">
        <div class="pie-identidad">
            <img src="/LogoIUB.png" alt="Logo IUB" />
            <div>
                <strong>BIENESTAR UNIVERSITARIO</strong>
                <span>Institución Universitaria de Barranquilla</span>
            </div>
        </div>

        <p>Promoviendo espacios para crecer, compartir y disfrutar.</p>

        <span class="copyright">© 2026 Bienestar Universitario</span>
    </footer>

</div>

<style>
    :global(*) {
        box-sizing: border-box;
    }

    :global(html) {
        scroll-behavior: smooth;
    }

    :global(body) {
        margin: 0;
        font-family: 'Nunito', sans-serif;
        color: #172344;
        background: #f5f7fc;
    }

    :global(button),
    :global(a) {
        font-family: 'Nunito', sans-serif;
    }

    .pagina {
        width: 100%;
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
    }

    .identidad {
        display: flex;
        align-items: center;
        gap: 13px;
        text-decoration: none;
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
        flex-shrink: 0;
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
        white-space: nowrap;
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
        border: none;
        background: transparent;
        color: white;
        font-size: 27px;
        cursor: pointer;
        padding: 5px 8px;
        border-radius: 8px;
    }

    /* PRESENTACIÓN */

    .presentacion {
        min-height: 355px;
        padding: 65px 10%;
        background: linear-gradient(115deg, #142044, #174d82);
        position: relative;
        display: flex;
        align-items: center;
        overflow: hidden;
    }

    .presentacion-contenido {
        position: relative;
        z-index: 2;
        max-width: 620px;
    }

    .etiqueta,
    .subtitulo {
        color: #00aef0;
        font-size: 13px;
        font-weight: 1000;
        letter-spacing: 2px;
    }

    .presentacion h1 {
        color: white;
        font-size: clamp(34px, 5vw, 55px);
        line-height: 1.12;
        font-weight: 1000;
        margin: 15px 0;
    }

    .presentacion h1 span {
        color: #f5ca24;
        display: block;
    }

    .presentacion p {
        color: #e0e8f5;
        font-size: 17px;
        font-weight: 800;
        line-height: 1.7;
        max-width: 510px;
    }

    .boton-descubrir {
        display: inline-flex;
        align-items: center;
        gap: 15px;
        margin-top: 18px;
        padding: 13px 23px;
        background: #f5ca24;
        color: #142044;
        text-decoration: none;
        border-radius: 9px;
        font-weight: 1000;
        transition: .2s;
    }

    .boton-descubrir:hover {
        background: white;
        transform: translateY(-3px);
    }

    .boton-descubrir span {
        font-size: 20px;
    }

    .presentacion-decoracion {
        position: absolute;
        right: 12%;
        top: 0;
        width: 350px;
        height: 100%;
    }

    .circulo {
        position: absolute;
        border-radius: 50%;
        border: 35px solid rgba(255,255,255,.06);
    }

    .circulo-uno {
        width: 310px;
        height: 310px;
        right: 0;
        top: 30px;
    }

    .circulo-dos {
        width: 190px;
        height: 190px;
        right: 60px;
        top: 90px;
        border-color: rgba(0,174,240,.18);
    }

    .figura-icono {
        position: absolute;
        right: 130px;
        top: 115px;
        font-size: 65px;
        color: #f5ca24;
    }

    /* CONTENIDO */

    .contenido {
        width: 100%;
        max-width: 1400px;
        margin: auto;
        padding: 75px 6%;
    }

    .titulo-seccion {
        display: flex;
        align-items: end;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 35px;
    }

    .titulo-textos {
        min-width: 0;
    }

    .titulo-seccion h2 {
        color: #142044;
        font-size: 36px;
        font-weight: 1000;
        margin: 7px 0;
    }

    .titulo-seccion p {
        color: #69758c;
        font-size: 16px;
        font-weight: 800;
        margin: 0;
    }

    /* FLECHAS */

    .controles {
        display: flex;
        align-items: center;
        gap: 13px;
        flex-shrink: 0;
    }

    .boton-carrusel {
        width: 49px;
        height: 49px;
        border: none;
        border-radius: 50%;
        background: #142044;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 5px 13px rgba(20,32,68,.18);
        transition: all .25s ease;
    }

    .boton-carrusel svg {
        width: 25px;
        height: 25px;
        stroke: currentColor;
        stroke-width: 3.5;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .boton-carrusel:hover {
        background: #f5ca24;
        color: #142044;
        transform: scale(1.1);
        box-shadow: 0 7px 17px rgba(245,202,36,.3);
    }

    .boton-carrusel:active {
        transform: scale(.94);
    }

    /* SWIPER */

    .carrusel-contenedor {
        width: 100%;
        padding: 15px 0 40px;
    }

    .eventos-swiper {
        width: 100%;
        padding: 25px 0 35px;
        overflow: visible;
    }

    .eventos-swiper .swiper-slide {
        height: 350px;
        border-radius: 18px;
        overflow: hidden;
        opacity: 1;
        transition: transform .35s ease;
    }

    :global(.eventos-swiper .swiper-slide-active) {
        z-index: 2;
    }

    .tarjeta-evento {
        width: 100%;
        height: 100%;
        position: relative;
        border-radius: 18px;
        overflow: hidden;
        background: #142044;
        box-shadow: 0 12px 30px rgba(15,32,65,.16);
    }

    .tarjeta-evento img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        opacity: 1;
        transition: transform .5s;
    }

    .tarjeta-evento:hover img {
        transform: scale(1.07);
    }

    .capa-tarjeta {
        position: absolute;
        inset: 0;
        padding: 22px;
        display: flex;
        flex-direction: column;
        justify-content: end;
        background: linear-gradient(transparent 30%, rgba(9,19,43,.9));
        color: white;
    }

    .categoria {
        align-self: flex-start;
        background: #f5ca24;
        color: #142044;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 1000;
        margin-bottom: 10px;
    }

    .capa-tarjeta h3 {
        font-size: 20px;
        font-weight: 1000;
        margin: 0 0 8px;
    }

    .ver-evento {
        font-size: 14px;
        font-weight: 900;
        color: #f5ca24;
    }

    .paginacion-eventos {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: 15px;
    }

    :global(.paginacion-eventos .swiper-pagination-bullet) {
        width: 9px;
        height: 9px;
        background: #aab4c6;
        opacity: 1;
    }

    :global(.paginacion-eventos .swiper-pagination-bullet-active) {
        width: 25px;
        border-radius: 10px;
        background: #00aef0;
    }

    /* DETALLE DEL EVENTO */

    .detalle-evento {
        display: grid;
        grid-template-columns: 1.1fr .9fr;
        gap: 55px;
        align-items: center;
        margin-top: 55px;
        padding: 45px;
        background: white;
        border-radius: 22px;
        box-shadow: 0 10px 35px rgba(20,32,68,.06);
    }

    .detalle-texto {
        min-width: 0;
    }

    .detalle-texto h2 {
        color: #142044;
        font-size: 34px;
        font-weight: 1000;
        margin: 10px 0 15px;
        overflow-wrap: break-word;
    }

    .descripcion {
        color: #69758c;
        font-size: 16px;
        line-height: 1.8;
        font-weight: 800;
    }

    .informacion-evento {
        display: grid;
        gap: 18px;
        margin: 28px 0;
    }

    .dato-evento {
        display: flex;
        align-items: center;
        gap: 14px;
        min-width: 0;
    }

    .dato-icono {
        width: 43px;
        height: 43px;
        border-radius: 12px;
        background: #eaf7ff;
        color: #008fcc;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 900;
        flex-shrink: 0;
    }

    .dato-evento div {
        display: flex;
        flex-direction: column;
        gap: 3px;
        min-width: 0;
    }

    .dato-evento small {
        color: #8a95a9;
        font-size: 12px;
        font-weight: 900;
    }

    .dato-evento strong {
        color: #142044;
        font-size: 14px;
        font-weight: 1000;
        overflow-wrap: anywhere;
    }

    .boton-inscripcion {
        padding: 14px 23px;
        background: #142044;
        color: white;
        border: none;
        border-radius: 9px;
        font-size: 15px;
        font-weight: 1000;
        cursor: pointer;
        transition: .2s;
    }

    .boton-inscripcion span {
        margin-left: 15px;
        color: #f5ca24;
        font-size: 19px;
    }

    .boton-inscripcion:hover {
        background: #00aef0;
        transform: translateY(-2px);
    }

    .mensaje {
        color: #00805b;
        font-weight: 900;
        font-size: 13px;
        margin-top: 15px;
    }

    .detalle-imagen {
        width: 100%;
        height: 390px;
        position: relative;
        border-radius: 18px;
        overflow: hidden;
    }

    .detalle-imagen img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .detalle-etiqueta {
        position: absolute;
        bottom: 20px;
        left: 20px;
        display: flex;
        flex-direction: column;
        background: #142044;
        color: white;
        padding: 13px 18px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 1000;
    }

    .detalle-etiqueta span {
        color: #f5ca24;
        letter-spacing: 2px;
    }

    /* PIE DE PÁGINA */

    .pie-pagina {
        background: #142044;
        padding: 35px 7%;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 25px;
        flex-wrap: wrap;
    }

    .pie-identidad {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .pie-identidad img {
        width: 48px;
        height: 48px;
        object-fit: contain;
        background: white;
        border-radius: 9px;
        padding: 4px;
        flex-shrink: 0;
    }

    .pie-identidad div {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .pie-identidad strong {
        font-size: 14px;
        font-weight: 1000;
    }

    .pie-identidad span,
    .pie-pagina p,
    .copyright {
        color: #bdc9dc;
        font-size: 12px;
        font-weight: 800;
    }

    /* TABLETAS */

    @media (max-width: 1000px) {
        .encabezado {
            padding-left: 4%;
            padding-right: 4%;
            gap: 15px;
        }

        .navegacion {
            gap: 20px;
        }

        .enlace {
            font-size: 14px;
        }

        .identidad-texto strong {
            font-size: 18px;
        }

        .identidad-texto span {
            font-size: 11px;
        }

        .presentacion-decoracion {
            right: -70px;
            opacity: .6;
        }

        .contenido {
            padding-left: 5%;
            padding-right: 5%;
        }

        .detalle-evento {
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            padding: 30px;
        }

        .detalle-imagen {
            height: 320px;
        }
    }

    /* TABLETAS PEQUEÑAS Y CELULARES */

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
            box-shadow: 0 10px 15px #0003;
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
            min-height: 330px;
            padding: 45px 7%;
        }

        .presentacion-contenido {
            max-width: 100%;
        }

        .presentacion h1 {
            font-size: clamp(32px, 7vw, 39px);
        }

        .presentacion p {
            font-size: 14px;
            max-width: 420px;
        }

        .presentacion-decoracion {
            right: -210px;
            opacity: .3;
        }

        .contenido {
            padding: 45px 5%;
        }

        .titulo-seccion {
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }

        .titulo-seccion h2 {
            font-size: 27px;
        }

        .titulo-seccion p {
            font-size: 13px;
            line-height: 1.5;
        }

        .subtitulo {
            font-size: 11px;
        }

        .controles {
            gap: 7px;
        }

        .boton-carrusel {
            width: 38px;
            height: 38px;
        }

        .boton-carrusel svg {
            width: 20px;
            height: 20px;
        }

        .carrusel-contenedor {
            padding-top: 5px;
        }

        .eventos-swiper .swiper-slide {
            height: 320px;
        }

        .capa-tarjeta {
            padding: 17px;
        }

        .capa-tarjeta h3 {
            font-size: 18px;
        }

        .detalle-evento {
            grid-template-columns: 1fr;
            gap: 25px;
            padding: 25px 20px;
            margin-top: 25px;
        }

        .detalle-texto h2 {
            font-size: 27px;
        }

        .descripcion {
            font-size: 14px;
        }

        .detalle-imagen {
            height: 260px;
        }

        .pie-pagina {
            padding: 30px 6%;
            flex-direction: column;
            align-items: flex-start;
            gap: 18px;
        }

        .pie-pagina p {
            margin: 0;
            line-height: 1.6;
        }
    }

    /* CELULARES */

    @media (max-width: 480px) {
        .encabezado {
            min-height: 68px;
        }

        .logo-contenedor {
            width: 41px;
            height: 41px;
        }

        .identidad-texto strong {
            font-size: 14px;
        }

        .identidad-texto span {
            font-size: 9px;
            letter-spacing: 1px;
        }

        .boton-menu {
            font-size: 25px;
        }

        .presentacion {
            min-height: 315px;
            padding: 40px 6%;
        }

        .etiqueta {
            font-size: 10px;
            letter-spacing: 1.5px;
        }

        .presentacion h1 {
            font-size: 33px;
        }

        .presentacion p {
            font-size: 13px;
            line-height: 1.6;
        }

        .boton-descubrir {
            padding: 11px 17px;
            font-size: 13px;
        }

        .contenido {
            padding: 38px 5%;
        }

        .titulo-seccion {
            align-items: flex-start;
        }

        .titulo-seccion h2 {
            font-size: 23px;
        }

        .titulo-seccion p {
            font-size: 12px;
        }

        .controles {
            gap: 5px;
        }

        .boton-carrusel {
            width: 33px;
            height: 33px;
        }

        .boton-carrusel svg {
            width: 17px;
            height: 17px;
        }

        .eventos-swiper .swiper-slide {
            height: 290px;
        }

        .categoria {
            font-size: 10px;
            padding: 5px 10px;
        }

        .capa-tarjeta h3 {
            font-size: 17px;
        }

        .detalle-evento {
            padding: 22px 17px;
        }

        .detalle-texto h2 {
            font-size: 24px;
        }

        .dato-evento strong {
            font-size: 12px;
        }

        .dato-icono {
            width: 39px;
            height: 39px;
        }

        .boton-inscripcion {
            width: 100%;
            padding: 13px 15px;
            font-size: 14px;
        }

        .detalle-imagen {
            height: 220px;
        }

        .detalle-etiqueta {
            bottom: 12px;
            left: 12px;
            padding: 10px 13px;
        }

        .pie-identidad strong {
            font-size: 12px;
        }

        .pie-identidad span {
            font-size: 10px;
        }
    }

    /* CELULARES MUY PEQUEÑOS */

    @media (max-width: 350px) {
        .identidad-texto strong {
            font-size: 12px;
        }

        .identidad-texto span {
            font-size: 8px;
        }

        .titulo-seccion {
            flex-wrap: wrap;
        }

        .controles {
            width: 100%;
            justify-content: flex-end;
        }

        .presentacion h1 {
            font-size: 29px;
        }

        .eventos-swiper .swiper-slide {
            height: 260px;
        }
    }
</style>
