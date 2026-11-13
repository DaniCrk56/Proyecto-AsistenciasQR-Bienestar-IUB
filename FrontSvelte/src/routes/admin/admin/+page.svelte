
<script>
    import { onMount } from 'svelte';

    let seccionActual = 'inicio';
    let eventos = [];
    let cargandoEventos = false;
    let mensajeEventos = '';
let estadisticas = {
    total_eventos: 0,
    eventos_activos: 0,
    estudiantes_inscritos: 0,
    total_asistencias: 0
};

let cargandoEstadisticas = false;
let mensajeEstadisticas = '';

    let asistencias = [];
let mostrarConfirmacion = false;
    let cargandoAsistencias = false;
    let mensajeAsistencias = '';
    let idEventoSeleccionado = '';

    let usuario = {
        nombres: '',
        apellidos: '',
        numero_documento: '',
        tipo_documento: '',
        correo_institucional: '',
        programa: '',
        id_rol: ''
    };

    let lugares = [];
    let categorias = [];
    let estados = [];

    let cargandoOpciones = false;
    let mensajeOpciones = '';

    let guardandoActividad = false;

let mostrarModalEdicion = false;
let eventoEditando = null;
let guardandoEdicion = false;
let mensajeEdicion = '';
let errorEdicion = false;

let mostrarConfirmacionEliminar = false;
let eventoEliminar = null;
let eliminandoEvento = false;
let mensajeEliminar = '';

    let mensajeActividad = '';
    let errorActividad = false;

    let nuevaActividad = {
        nombre: '',
        descripcion: '',
        fecha: '',
        hora_inicio: '',
        hora_fin: '',
        cupo_maximo: '',
        id_lugar: '',
        id_categoria: '',
        id_estado_actividad: ''
    };

let actividadEditada = {
    nombre: '',
    descripcion: '',
    fecha: '',
    hora_inicio: '',
    hora_fin: '',
    cupo_maximo: '',
    id_lugar: '',
    id_categoria: '',
    id_estado_actividad: '',
    id_responsable: null
};

    const URL_BASE = 'https://proyecto-asistenciasqr-bienestar-iub.onrender.com';

    let opciones = [
        { id: 'inicio', nombre: 'Panel principal', icono: '⌂' },
        { id: 'crear', nombre: 'Crear evento', icono: '＋' },
        { id: 'eventos', nombre: 'Gestionar eventos', icono: '▦' },
        { id: 'scanner', nombre: 'Escanear QR', icono: '▣' },
        { id: 'asistencia', nombre: 'Asistencias', icono: '☷' },
        { id: 'perfil', nombre: 'Mi perfil', icono: '♙' }
    ];

    function cargarUsuario() {
        const usuarioGuardado = localStorage.getItem('usuario');

        if (usuarioGuardado) {
            usuario = JSON.parse(usuarioGuardado);
        }
    }


async function cargarEstadisticas() {
    cargandoEstadisticas = true;
    mensajeEstadisticas = '';

    try {
        const token = localStorage.getItem('token');

        const respuesta = await fetch(
            URL_BASE + '/actividades/estadisticas/panel',
            {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            }
        );

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                datos.detail || 'No se pudieron cargar las estadísticas.'
            );
        }

        estadisticas = datos;

    } catch (error) {
        mensajeEstadisticas =
            error.message || 'Error al consultar las estadísticas.';
    }

    cargandoEstadisticas = false;
}


    onMount(() => {
    cargarUsuario();
    cargarEstadisticas();
});

    function cambiarSeccion(seccion) {
        seccionActual = seccion;

        if (seccion === 'crear') {
            cargarOpciones();
        }

        if (
            seccion === 'eventos' ||
            seccion === 'scanner' ||
            seccion === 'asistencia'
        ) {
            cargarEventos();
        }
    }

function abrirEdicion(evento) {
    eventoEditando = evento;

    actividadEditada = {
        nombre: evento.nombre || '',
        descripcion: evento.descripcion || '',
        fecha: evento.fecha ? String(evento.fecha).substring(0, 10) : '',
        hora_inicio: evento.hora_inicio ? String(evento.hora_inicio).substring(0, 5) : '',
        hora_fin: evento.hora_fin ? String(evento.hora_fin).substring(0, 5) : '',
        cupo_maximo: evento.cupo_maximo,
        id_lugar: evento.id_lugar,
        id_categoria: evento.id_categoria,
        id_estado_actividad: evento.id_estado_actividad,
        id_responsable: evento.id_responsable ?? null
    };

    mensajeEdicion = '';
    errorEdicion = false;
    mostrarModalEdicion = true;

    if (lugares.length === 0 || categorias.length === 0 || estados.length === 0) {
        cargarOpciones();
    }
}

function cerrarEdicion() {
    mostrarModalEdicion = false;
    eventoEditando = null;
    mensajeEdicion = '';
}

async function guardarEdicion() {
    if (!eventoEditando) return;

    guardandoEdicion = true;
    mensajeEdicion = '';
    errorEdicion = false;

    const token = localStorage.getItem('token');

    const datos = {
        nombre: actividadEditada.nombre,
        descripcion: actividadEditada.descripcion,
        fecha: actividadEditada.fecha,
        hora_inicio: actividadEditada.hora_inicio,
        hora_fin: actividadEditada.hora_fin,
        cupo_maximo: Number(actividadEditada.cupo_maximo),
        id_lugar: Number(actividadEditada.id_lugar),
        id_categoria: Number(actividadEditada.id_categoria),
        id_estado_actividad: Number(actividadEditada.id_estado_actividad),
        id_responsable: actividadEditada.id_responsable
    };

    try {
        const respuesta = await fetch(`${URL_BASE}/actividades/${eventoEditando.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(resultado.detail || 'No se pudo actualizar el evento');
        }

        mensajeEdicion = 'Evento actualizado correctamente';
        await cargarEventos();

        setTimeout(() => {
            cerrarEdicion();
        }, 1000);

    } catch (error) {
        errorEdicion = true;
        mensajeEdicion = error.message;
    } finally {
        guardandoEdicion = false;
    }
}

function confirmarEliminar(evento) {
    eventoEliminar = evento;
    mensajeEliminar = '';
    mostrarConfirmacionEliminar = true;
}

function cancelarEliminar() {
    mostrarConfirmacionEliminar = false;
    eventoEliminar = null;
    mensajeEliminar = '';
}

async function eliminarEvento() {
    if (!eventoEliminar) return;

    eliminandoEvento = true;
    mensajeEliminar = '';

    const token = localStorage.getItem('token');

    try {
        const respuesta = await fetch(`${URL_BASE}/actividades/${eventoEliminar.id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(resultado.detail || 'No se pudo eliminar el evento');
        }

        await cargarEventos();
        cancelarEliminar();

    } catch (error) {
        mensajeEliminar = error.message;
    } finally {
        eliminandoEvento = false;
    }
}

function cerrarSesion() {
    mostrarConfirmacion = false;
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    window.location.href = '/';
}

function cancelarCierre() {
    mostrarConfirmacion = false;
}

    async function cargarOpciones() {
        cargandoOpciones = true;
        mensajeOpciones = '';

        try {
            const respuestaLugares = await fetch(URL_BASE + '/lugares/');
            const respuestaCategorias = await fetch(URL_BASE + '/categorias-actividad/');
            const respuestaEstados = await fetch(URL_BASE + '/estados-actividad/');

            if (
                !respuestaLugares.ok ||
                !respuestaCategorias.ok ||
                !respuestaEstados.ok
            ) {
                throw new Error('No se pudieron cargar las opciones.');
            }

            lugares = await respuestaLugares.json();
            categorias = await respuestaCategorias.json();
            estados = await respuestaEstados.json();

        } catch (error) {
            mensajeOpciones = error.message || 'Error al cargar los datos.';
        }

        cargandoOpciones = false;
    }

    async function cargarEventos() {
        cargandoEventos = true;
        mensajeEventos = '';

        try {
            const respuesta = await fetch(URL_BASE + '/actividades/');

            if (!respuesta.ok) {
                throw new Error('No se pudieron cargar los eventos.');
            }

            eventos = await respuesta.json();

        } catch (error) {
            mensajeEventos = error.message || 'Error al cargar los eventos.';
        }

        cargandoEventos = false;
    }

    async function cargarAsistencias(idEvento) {
        if (!idEvento) {
            asistencias = [];
            mensajeAsistencias = '';
            return;
        }

        cargandoAsistencias = true;
        mensajeAsistencias = '';
        asistencias = [];

        try {
            const token = localStorage.getItem('token');

            const respuesta = await fetch(
                URL_BASE + '/asistencias/evento/' + idEvento,
                {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + token
                    }
                }
            );

            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(
                    datos.detail || 'No se pudieron consultar las asistencias.'
                );
            }

            asistencias = datos;

        } catch (error) {
            mensajeAsistencias =
                error.message || 'Error al consultar las asistencias.';
        }

        cargandoAsistencias = false;
    }

    async function crearActividad(evento) {
        evento.preventDefault();

        mensajeActividad = '';
        errorActividad = false;
        guardandoActividad = true;

        try {
            const respuesta = await fetch(URL_BASE + '/actividades/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nombre: nuevaActividad.nombre,
                    descripcion: nuevaActividad.descripcion,
                    fecha: nuevaActividad.fecha,
                    hora_inicio: nuevaActividad.hora_inicio,
                    hora_fin: nuevaActividad.hora_fin,
                    cupo_maximo: Number(nuevaActividad.cupo_maximo),
                    id_lugar: Number(nuevaActividad.id_lugar),
                    id_categoria: Number(nuevaActividad.id_categoria),
                    id_estado_actividad: Number(nuevaActividad.id_estado_actividad)
                })
            });

            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(datos.detail || 'No se pudo registrar el evento.');
            }

            mensajeActividad = '¡Evento registrado correctamente!';

            await cargarEventos();

            nuevaActividad = {
                nombre: '',
                descripcion: '',
                fecha: '',
                hora_inicio: '',
                hora_fin: '',
                cupo_maximo: '',
                id_lugar: '',
                id_categoria: '',
                id_estado_actividad: ''
            };

        } catch (error) {
            errorActividad = true;
            mensajeActividad =
                error.message || 'Ocurrió un error al registrar el evento.';
        }

        guardandoActividad = false;
    }

    function abrirScanner(evento) {
        window.location.href = '/admin/scanner?id_evento=' + evento.id;
    }
</script>

<svelte:head>
    <title>Panel administrativo | Bienestar Universitario</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900;1000&display=swap" rel="stylesheet">
</svelte:head>

<div class="panel">

    <aside class="barra-lateral">
        <div class="marca">
            <img src="/LogoIUB.png" alt="Logo IUB">
            <div>
                <h2>BIENESTAR</h2>
                <span>UNIVERSITARIO</span>
            </div>
        </div>

        <div class="separador"></div>

        <p class="titulo-menu">MENÚ PRINCIPAL</p>

        <nav>
            {#each opciones as opcion}
                <button
                    class:activo={seccionActual === opcion.id}
                    onclick={() => cambiarSeccion(opcion.id)}
                >
                    <span class="icono">{opcion.icono}</span>
                    {opcion.nombre}
                </button>
            {/each}
        </nav>

        <div class="parte-inferior">
            <div class="separador"></div>

            <div class="usuario">
                <div class="avatar">
                    {usuario.nombres ? usuario.nombres.charAt(0).toUpperCase() : 'A'}
                </div>

                <div>
                    <strong>{usuario.nombres || 'Administrador'} {usuario.apellidos || ''}</strong>
                    <span>Panel administrativo</span>
                </div>
            </div>
        </div>
    </aside>

    <main class="contenido">

        <header class="encabezado">
            <div>
                <span class="subtitulo">BIENESTAR UNIVERSITARIO</span>
                <h1>
                    {#if seccionActual === 'inicio'}
                        Panel principal
                    {:else if seccionActual === 'crear'}
                        Crear evento
                    {:else if seccionActual === 'eventos'}
                        Gestionar eventos
                    {:else if seccionActual === 'scanner'}
                        Escanear QR
                    {:else if seccionActual === 'asistencia'}
                        Asistencias
                    {:else}
                        Mi perfil
                    {/if}
                </h1>
            </div>

            <div class="fecha-actual">
                <span>●</span> Panel de administración
            </div>
        </header>

        {#if seccionActual === 'inicio'}

            <section class="bienvenida">
                <div>
                    <span>ADMINISTRACIÓN</span>
                    <h2>¡Bienvenido al panel de gestión!</h2>
                    <p>Administra los eventos universitarios y supervisa la asistencia de los estudiantes desde un solo lugar.</p>
                </div>
                <div class="bienvenida-icono">✦</div>
            </section>

           
<section class="estadisticas">

    <article class="estadistica">
        <div class="estadistica-icono azul">▦</div>
        <span>Total de eventos</span>
        <h2>
            {cargandoEstadisticas ? '...' : estadisticas.total_eventos}
        </h2>
        <small>Eventos registrados</small>
    </article>

    <article class="estadistica">
        <div class="estadistica-icono verde">✓</div>
        <span>Eventos activos</span>
        <h2>
            {cargandoEstadisticas ? '...' : estadisticas.eventos_activos}
        </h2>
        <small>Disponibles actualmente</small>
    </article>

    <article class="estadistica">
        <div class="estadistica-icono amarillo">♙</div>
        <span>Estudiantes inscritos</span>
        <h2>
            {cargandoEstadisticas ? '...' : estadisticas.estudiantes_inscritos}
        </h2>
        <small>Inscripciones registradas</small>
    </article>

    <article class="estadistica">
        <div class="estadistica-icono morado">▣</div>
        <span>Asistencias</span>
        <h2>
            {cargandoEstadisticas ? '...' : estadisticas.total_asistencias}
        </h2>
        <small>Asistencias registradas</small>
    </article>

</section>

{#if mensajeEstadisticas}
    <p class="error-mensaje">{mensajeEstadisticas}</p>
{/if}


            <section class="seccion">
                <div class="encabezado-seccion">
                    <div>
                        <h2>Accesos rápidos</h2>
                        <p>Selecciona una función para comenzar.</p>
                    </div>
                </div>

                <div class="accesos">
                    <button onclick={() => cambiarSeccion('crear')}>
                        <span class="acceso-icono">＋</span>
                        <strong>Crear evento</strong>
                        <small>Registrar una nueva actividad</small>
                        <span class="flecha">→</span>
                    </button>

                    <button onclick={() => cambiarSeccion('scanner')}>
                        <span class="acceso-icono">▣</span>
                        <strong>Escanear QR</strong>
                        <small>Validar asistencia de estudiantes</small>
                        <span class="flecha">→</span>
                    </button>

                    <button onclick={() => cambiarSeccion('asistencia')}>
                        <span class="acceso-icono">☷</span>
                        <strong>Consultar asistencias</strong>
                        <small>Revisar registros de asistencia</small>
                        <span class="flecha">→</span>
                    </button>
                </div>
            </section>

        {:else if seccionActual === 'scanner'}

            <section class="introduccion">
                <h2>Selecciona un evento para escanear</h2>
                <p>Busca la actividad correspondiente y abre su lector de códigos QR.</p>
            </section>

            {#if cargandoEventos}
                <p>Cargando eventos...</p>
            {:else if mensajeEventos}
                <p class="error-mensaje">{mensajeEventos}</p>
            {:else if eventos.length === 0}
                <section class="seccion-vacia">
                    <div class="vacio-icono">▦</div>
                    <h2>No hay eventos registrados</h2>
                    <p>Primero debes crear un evento.</p>
                </section>
            {:else}
                <div class="tarjetas-eventos">
                    {#each eventos as evento}
                        <article class="tarjeta-evento">
                            <div class="imagen-evento">
                                <span>EVENTO UNIVERSITARIO</span>
                                <div class="imagen-decoracion">✦</div>
                            </div>

                            <div class="informacion-evento">
                                <span class="categoria">Evento #{evento.id}</span>
                                <h3>{evento.nombre}</h3>

                                <p>◷ Fecha: {evento.fecha}</p>
                                <p>◴ Hora: {evento.hora_inicio.slice(0, 5)} - {evento.hora_fin.slice(0, 5)}</p>

                                <button class="boton-escanear" onclick={() => abrirScanner(evento)}>
                                    ▣ Escanear QR
                                </button>
                            </div>
                        </article>
                    {/each}
                </div>
            {/if}

        {:else if seccionActual === 'crear'}

            <section class="seccion">
                <div class="encabezado-seccion">
                    <h2>Registrar nueva actividad</h2>
                    <p>Completa los datos para publicar un evento universitario.</p>
                </div>

                {#if cargandoOpciones}
                    <p>Cargando información...</p>
                {:else if mensajeOpciones}
                    <p class="error-mensaje">{mensajeOpciones}</p>
                {:else}
                    <form class="formulario-evento" onsubmit={crearActividad}>

                        <label>Nombre del evento</label>
                        <input bind:value={nuevaActividad.nombre} required placeholder="Nombre de la actividad">

                        <label>Descripción</label>
                        <textarea bind:value={nuevaActividad.descripcion} placeholder="Describe la actividad"></textarea>

                        <div class="campos-dobles">
                            <div>
                                <label>Fecha</label>
                                <input type="date" bind:value={nuevaActividad.fecha} required>
                            </div>

                            <div>
                                <label>Cupo máximo</label>
                                <input type="number" min="1" bind:value={nuevaActividad.cupo_maximo} required>
                            </div>
                        </div>

                        <div class="campos-dobles">
                            <div>
                                <label>Hora de inicio</label>
                                <input type="time" bind:value={nuevaActividad.hora_inicio} required>
                            </div>

                            <div>
                                <label>Hora de finalización</label>
                                <input type="time" bind:value={nuevaActividad.hora_fin} required>
                            </div>
                        </div>

                        <label>Lugar</label>
                        <select bind:value={nuevaActividad.id_lugar} required>
                            <option value="">Selecciona un lugar</option>
                            {#each lugares as lugar}
                                <option value={lugar.id}>{lugar.nombre}</option>
                            {/each}
                        </select>

                        <label>Categoría</label>
                        <select bind:value={nuevaActividad.id_categoria} required>
                            <option value="">Selecciona una categoría</option>
                            {#each categorias as categoria}
                                <option value={categoria.id}>{categoria.nombre}</option>
                            {/each}
                        </select>

                        <label>Estado de la actividad</label>
                        <select bind:value={nuevaActividad.id_estado_actividad} required>
                            <option value="">Selecciona un estado</option>
                            {#each estados as estado}
                                <option value={estado.id}>{estado.nombre}</option>
                            {/each}
                        </select>

                        {#if mensajeActividad}
                            <p class:error-mensaje={errorActividad} class:exito-mensaje={!errorActividad}>
                                {mensajeActividad}
                            </p>
                        {/if}

                        <button type="submit" disabled={guardandoActividad}>
                            {guardandoActividad ? 'Guardando...' : '＋ Crear evento'}
                        </button>

                    </form>
                {/if}
            </section>

        {:else if seccionActual === 'eventos'}

            <section class="seccion">
                <div class="encabezado-seccion">
                    <h2>Eventos registrados</h2>
                    <p>Consulta las actividades universitarias que has creado.</p>
                </div>

                {#if cargandoEventos}
                    <p>Cargando eventos...</p>

                {:else if mensajeEventos}
                    <p class="error-mensaje">{mensajeEventos}</p>

                {:else if eventos.length === 0}
                    <section class="seccion-vacia">
                        <div class="vacio-icono">▦</div>
                        <h2>No hay eventos registrados</h2>
                        <p>Cuando crees una actividad, aparecerá aquí.</p>
                    </section>

                {:else}
                    <div class="tarjetas-eventos">
                        {#each eventos as evento}
                            <article class="tarjeta-evento">

                                <div class="imagen-evento">
                                    <span>EVENTO UNIVERSITARIO</span>
                                    <div class="imagen-decoracion">✦</div>
                                </div>

                                <div class="informacion-evento">

                                    <span class="categoria">
                                        Evento #{evento.id}
                                    </span>

                                    <h3>{evento.nombre}</h3>

                                    <p>{evento.descripcion || 'Sin descripción disponible.'}</p>

                                    <p>◷ Fecha: {evento.fecha}</p>

                                    <p>
                                        ◴ Horario: {evento.hora_inicio.slice(0, 5)}
                                        - {evento.hora_fin.slice(0, 5)}
                                    </p>

                                    <p>♙ Cupos: {evento.cupo_maximo}</p>

                                    <p>⌖ Lugar ID: {evento.id_lugar}</p>

                                    <p>▦ Categoría ID: {evento.id_categoria}</p>

                                    <p>
                                        Estado:
                                        {evento.estado ? 'Activo' : 'Inactivo'}
                                    </p>
<div class="acciones-evento">
    <button
        class="btn-editar"
        onclick={() => abrirEdicion(evento)}
    >
        Editar
    </button>

    <button
        class="btn-eliminar"
        onclick={() => confirmarEliminar(evento)}
    >
        Eliminar
    </button>
</div>
                                </div>
                            </article>
                        {/each}
                    </div>
                {/if}
            </section>

        {:else if seccionActual === 'perfil'}

            <section class="seccion-vacia perfil">

                <div class="vacio-icono">♙</div>

                <h2>Mi perfil</h2>
                <p>Información de tu cuenta institucional.</p>

                <div class="datos-perfil">

                    <div class="dato-perfil">
                        <span>Nombres</span>
                        <strong>{usuario.nombres || 'No disponible'}</strong>
                    </div>

                    <div class="dato-perfil">
                        <span>Apellidos</span>
                        <strong>{usuario.apellidos || 'No disponible'}</strong>
                    </div>

                    <div class="dato-perfil">
                        <span>Tipo de documento</span>
                        <strong>{usuario.tipo_documento || 'No disponible'}</strong>
                    </div>

                    <div class="dato-perfil">
                        <span>Número de documento</span>
                        <strong>{usuario.numero_documento || 'No disponible'}</strong>
                    </div>

                    <div class="dato-perfil">
                        <span>Correo institucional</span>
                        <strong>{usuario.correo_institucional || 'No disponible'}</strong>
                    </div>

                    <div class="dato-perfil">
                        <span>Programa</span>
                        <strong>{usuario.programa || 'No disponible'}</strong>
                    </div>

                    <div class="dato-perfil">
                        <span>Rol</span>
                        <strong>{usuario.id_rol === 1 ? 'Administrador' : 'Usuario'}</strong>
                    </div>

                </div>

           <button class="boton-cerrar-sesion" onclick={() => mostrarConfirmacion = true}>
    <span>↪</span>
    Cerrar sesión
</button>

            </section>

        {:else if seccionActual === 'asistencia'}

            <section class="seccion">

                <div class="encabezado-seccion">
                    <h2>Gestión de asistencias</h2>
                    <p>Consulta los estudiantes que asistieron a cada evento universitario.</p>
                </div>

                <div class="formulario-evento">

                    <label>Seleccionar evento</label>

                    <select
                        bind:value={idEventoSeleccionado}
                        onchange={() => cargarAsistencias(Number(idEventoSeleccionado))}
                    >
                        <option value="">Selecciona un evento</option>

                        {#each eventos as evento}
                            <option value={evento.id}>
                                {evento.nombre}
                            </option>
                        {/each}

                    </select>

                </div>

                {#if cargandoEventos}

                    <p>Cargando eventos...</p>

                {:else if mensajeEventos}

                    <p class="error-mensaje">{mensajeEventos}</p>

                {:else if eventos.length === 0}

                    <section class="seccion-vacia">
                        <div class="vacio-icono">▦</div>
                        <h2>No hay eventos registrados</h2>
                        <p>Primero debes crear un evento.</p>
                    </section>

                {:else if idEventoSeleccionado}

                    <section class="seccion">

                        <div class="encabezado-seccion">
                            <h2>Estudiantes asistentes</h2>
                            <p>Total de asistencias: {asistencias.length}</p>
                        </div>

                        {#if cargandoAsistencias}

                            <p>Consultando asistencias...</p>

                        {:else if mensajeAsistencias}

                            <p class="error-mensaje">{mensajeAsistencias}</p>

                        {:else if asistencias.length === 0}

                            <section class="seccion-vacia">
                                <div class="vacio-icono">☷</div>
                                <h2>Sin asistencias registradas</h2>
                                <p>Todavía no hay estudiantes con asistencia registrada en este evento.</p>
                            </section>

                        {:else}

                            <div class="tabla-asistencias">

                                <table>
                                    <thead>
                                        <tr>
                                            <th>Estudiante</th>
                                            <th>Documento</th>
                                            <th>Fecha y hora</th>
                                            <th>Método</th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {#each asistencias as asistencia}
                                            <tr>
                                                <td>
                                                    {asistencia.nombres} {asistencia.apellidos}
                                                </td>

                                                <td>{asistencia.numero_documento}</td>

                                                <td>
                                                    {new Date(asistencia.fecha_asistencia).toLocaleString('es-CO')}
                                                </td>

                                                <td>
                                                    <span class="metodo-qr">
                                                        {asistencia.metodo}
                                                    </span>
                                                </td>
                                            </tr>
                                        {/each}
                                    </tbody>
                                </table>

                            </div>

                        {/if}

                    </section>

                {/if}

            </section>

        {/if}

    </main>
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
    :global(*) {
        box-sizing: border-box;
    }

    :global(body) {
        margin: 0;
        font-family: 'Nunito', sans-serif;
        background: #f3f6fc;
    }

    .panel {
        display: flex;
        min-height: 100vh;
        width: 100%;
        color: #18233f;
    }

    .barra-lateral {
        width: 270px;
        min-width: 270px;
        background: #111c3b;
        color: white;
        padding: 28px 18px;
        display: flex;
        flex-direction: column;
    }

    .marca {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 8px;
    }

    .marca img {
        width: 48px;
        height: 48px;
        object-fit: contain;
        background: white;
        border-radius: 12px;
        padding: 4px;
    }

    .marca h2 {
        font-size: 15px;
        font-weight: 1000;
        margin: 0;
    }

    .marca span {
        font-size: 10px;
        letter-spacing: 2px;
        color: #aab8d0;
        font-weight: 800;
    }

    .separador {
        height: 1px;
        background: #34415f;
        margin: 28px 0;
    }

    .titulo-menu {
        font-size: 10px;
        color: #8795b2;
        font-weight: 900;
        letter-spacing: 1.5px;
        padding-left: 12px;
        margin-bottom: 15px;
    }

    nav {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    nav button,
    .cerrar {
        display: flex;
        align-items: center;
        gap: 13px;
        width: 100%;
        border: none;
        background: transparent;
        color: #b9c5dc;
        padding: 14px 13px;
        border-radius: 12px;
        font-family: inherit;
        font-size: 14px;
        font-weight: 800;
        text-align: left;
        cursor: pointer;
        transition: 0.2s;
    }

    nav button:hover,
    .cerrar:hover {
        background: #1c2a4e;
        color: white;
    }

    nav button.activo {
        background: #0785b6;
        color: white;
        box-shadow: 0 6px 18px #0785b644;
    }

    .icono {
        font-size: 21px;
        width: 24px;
        text-align: center;
    }

    .parte-inferior {
        margin-top: auto;
    }

    .usuario {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 15px 8px 0;
    }

    .avatar {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: #0785b6;
        font-weight: 1000;
    }

    .usuario strong,
    .usuario span {
        display: block;
    }

    .usuario strong {
        font-size: 13px;
    }

    .usuario span {
        font-size: 10px;
        color: #aab8d0;
    }

    .contenido {
        flex: 1;
        min-width: 0;
        padding: 35px 45px;
    }

    .encabezado {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        gap: 15px;
    }

    .subtitulo {
        color: #0785b6;
        font-size: 10px;
        font-weight: 1000;
        letter-spacing: 2px;
    }

    .encabezado h1 {
        margin: 4px 0 0;
        font-size: 29px;
        font-weight: 1000;
    }

    .fecha-actual {
        background: white;
        padding: 12px 18px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 800;
        color: #596781;
        box-shadow: 0 4px 15px #15264a0a;
    }

    .fecha-actual span {
        color: #18b67b;
        margin-right: 5px;
    }

    .bienvenida {
        background: linear-gradient(115deg, #0785b6, #07517f);
        padding: 35px;
        border-radius: 20px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        overflow: hidden;
        min-height: 190px;
    }

    .bienvenida span {
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #c9edff;
    }

    .bienvenida h2 {
        font-size: 25px;
        font-weight: 1000;
        margin: 8px 0;
    }

    .bienvenida p {
        max-width: 560px;
        font-size: 13px;
        line-height: 1.7;
        color: #e4f5ff;
    }

    .bienvenida-icono {
        font-size: 90px;
        opacity: 0.25;
        margin-right: 25px;
    }

    .estadisticas {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin: 25px 0 35px;
    }

    .estadistica {
        background: white;
        padding: 22px;
        border-radius: 17px;
        box-shadow: 0 5px 20px #15264a08;
    }

    .estadistica-icono {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: grid;
        place-items: center;
        font-size: 21px;
        margin-bottom: 15px;
    }

    .azul { background: #e4f3ff; color: #0785b6; }
    .verde { background: #e2f8ed; color: #159a65; }
    .amarillo { background: #fff5d9; color: #d69a00; }
    .morado { background: #f0eaff; color: #7954cf; }

    .estadistica > span {
        color: #74809a;
        font-size: 12px;
        font-weight: 800;
    }

    .estadistica h2 {
        margin: 5px 0;
        font-size: 29px;
        font-weight: 1000;
    }

    .estadistica small {
        color: #9ba5b8;
        font-size: 10px;
    }

    .encabezado-seccion {
        margin-bottom: 18px;
    }

    .encabezado-seccion h2,
    .introduccion h2 {
        font-size: 20px;
        font-weight: 1000;
        margin: 0;
    }

    .encabezado-seccion p,
    .introduccion p {
        color: #8590a6;
        font-size: 12px;
    }

    .accesos {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
    }

    .accesos button {
        position: relative;
        background: white;
        border: 1px solid #e9edf5;
        border-radius: 17px;
        padding: 23px;
        text-align: left;
        font-family: inherit;
        cursor: pointer;
        transition: 0.25s;
    }

    .accesos button:hover {
        transform: translateY(-4px);
        border-color: #0785b6;
        box-shadow: 0 10px 25px #0785b615;
    }

    .acceso-icono {
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: #e7f5fc;
        color: #0785b6;
        font-size: 25px;
        margin-bottom: 16px;
    }

    .accesos strong,
    .accesos small {
        display: block;
    }

    .accesos strong {
        font-size: 14px;
        color: #18233f;
        font-weight: 1000;
    }

    .accesos small {
        font-size: 11px;
        color: #929db1;
        margin-top: 5px;
    }

    .flecha {
        position: absolute;
        right: 20px;
        bottom: 20px;
        color: #0785b6;
        font-size: 20px;
    }

    .introduccion {
        margin-bottom: 25px;
    }

    .tarjetas-eventos {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 22px;
    }

    .tarjeta-evento {
        background: white;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 5px 20px #15264a0a;
        transition: 0.25s;
    }

    .tarjeta-evento:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 25px #15264a15;
    }

    .imagen-evento {
        height: 135px;
        background: linear-gradient(120deg, #0785b6, #13244c);
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        padding: 18px;
        color: white;
    }

    .imagen-evento > span {
        font-size: 9px;
        letter-spacing: 1px;
        font-weight: 900;
    }

    .imagen-decoracion {
        font-size: 50px;
        opacity: 0.3;
    }

    .informacion-evento {
        padding: 20px;
    }

    .categoria {
        color: #0785b6;
        font-size: 10px;
        font-weight: 1000;
        text-transform: uppercase;
    }

    .informacion-evento h3 {
        font-size: 17px;
        font-weight: 1000;
        margin: 7px 0 15px;
    }

    .informacion-evento p {
        color: #77839a;
        font-size: 11px;
        margin: 9px 0;
    }

    .boton-escanear {
        width: 100%;
        margin-top: 15px;
        padding: 13px;
        border: none;
        border-radius: 11px;
        background: #0785b6;
        color: white;
        font-family: inherit;
        font-weight: 1000;
        font-size: 12px;
        cursor: pointer;
        transition: 0.2s;
    }

    .boton-escanear:hover {
        background: #056b91;
    }

    .seccion-vacia {
        background: white;
        padding: 65px 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 5px 20px #15264a08;
    }

    .vacio-icono {
        margin: 0 auto 15px;
        display: grid;
        place-items: center;
        width: 65px;
        height: 65px;
        border-radius: 20px;
        background: #e7f5fc;
        color: #0785b6;
        font-size: 32px;
    }

    .seccion-vacia h2 {
        font-weight: 1000;
    }

    .seccion-vacia p {
        color: #8995a9;
        font-size: 13px;
    }

    .formulario-evento {
        background: white;
        padding: 30px;
        border-radius: 18px;
        max-width: 850px;
        box-shadow: 0 5px 20px #15264a08;
    }

    .formulario-evento label {
        display: block;
        margin: 18px 0 7px;
        font-size: 13px;
        font-weight: 900;
        color: #34415f;
    }

    .formulario-evento input,
    .formulario-evento textarea,
    .formulario-evento select {
        width: 100%;
        padding: 13px;
        border: 1px solid #dfe5ef;
        border-radius: 10px;
        font-family: inherit;
        font-size: 13px;
        outline: none;
    }

    .formulario-evento input:focus,
    .formulario-evento textarea:focus,
    .formulario-evento select:focus {
        border-color: #0785b6;
    }

    .formulario-evento textarea {
        min-height: 100px;
        resize: vertical;
    }

    .campos-dobles {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 18px;
    }

    .formulario-evento button {
        width: 100%;
        margin-top: 25px;
        padding: 15px;
        background: #0785b6;
        color: white;
        border: none;
        border-radius: 10px;
        font-family: inherit;
        font-weight: 1000;
        cursor: pointer;
    }

    .formulario-evento button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .error-mensaje {
        color: #d93636;
    }

    .exito-mensaje {
        color: #159a65;
    }

    .boton-cerrar-sesion {
        margin-top: 25px;
        padding: 13px 25px;
        border: none;
        border-radius: 10px;
        background: #0785b6;
        color: white;
        font-family: inherit;
        font-size: 13px;
        font-weight: 900;
        cursor: pointer;
        transition: 0.2s;
    }

    .boton-cerrar-sesion:hover {
        background: #056b91;
        transform: translateY(-2px);
    }

    .boton-cerrar-sesion span {
        margin-right: 8px;
        font-size: 17px;
    }

    .datos-perfil {
        max-width: 650px;
        margin: 30px auto 0;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        text-align: left;
    }

    .dato-perfil {
        background: #f5f8fc;
        padding: 17px;
        border-radius: 12px;
        border: 1px solid #e7edf5;
    }

    .dato-perfil span {
        display: block;
        color: #8995a9;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .dato-perfil strong {
        display: block;
        color: #18233f;
        font-size: 13px;
        overflow-wrap: anywhere;
    }

    @media (max-width: 1100px) {
        .estadisticas {
            grid-template-columns: repeat(2, 1fr);
        }

        .tarjetas-eventos {
            grid-template-columns: repeat(2, 1fr);
        }

        .contenido {
            padding: 30px 25px;
        }
    }

    @media (max-width: 750px) {
        .panel {
            flex-direction: column;
        }

        .barra-lateral {
            width: 100%;
            min-width: 0;
            padding: 18px;
        }

        nav {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
        }

        .parte-inferior {
            margin-top: 15px;
        }

        .contenido {
            padding: 25px 18px;
        }

        .encabezado {
            align-items: flex-start;
            flex-direction: column;
        }

        .estadisticas,
        .accesos,
        .tarjetas-eventos {
            grid-template-columns: 1fr;
        }

        .bienvenida {
            padding: 25px;
        }

        .bienvenida h2 {
            font-size: 21px;
        }

        .bienvenida-icono {
            display: none;
        }
    }

    @media (max-width: 600px) {
        .datos-perfil,
        .campos-dobles {
            grid-template-columns: 1fr;
        }
    }

    .tabla-asistencias {
        width: 100%;
        overflow-x: auto;
        background: white;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 5px 20px #15264a08;
    }

    .tabla-asistencias table {
        width: 100%;
        border-collapse: collapse;
        min-width: 650px;
    }

    .tabla-asistencias th,
    .tabla-asistencias td {
        padding: 16px;
        text-align: left;
        border-bottom: 1px solid #edf0f5;
        font-size: 12px;
    }

    .tabla-asistencias th {
        background: #f5f8fc;
        color: #34415f;
        font-weight: 1000;
    }

    .tabla-asistencias td {
        color: #66738a;
    }

    .metodo-qr {
        background: #e2f8ed;
        color: #159a65;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 1000;
    }

.modal-fondo {
    position: fixed;
    top: 0;
    left: 0;
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
