
<script>
    import { afterNavigate } from '$app/navigation';
    import { onMount } from 'svelte';

    function cerrarSesion() {
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');

        window.location.replace('/');
    }

    function verificarSesion() {
        const ruta = window.location.pathname;

        if (ruta === '/' || ruta === '/registro') {
            return;
        }

        const token = localStorage.getItem('token');
        const usuario = localStorage.getItem('usuario');

        if (!token || !usuario) {
            cerrarSesion();
            return;
        }

        try {
            const partes = token.split('.');
            const datos = JSON.parse(atob(partes[1]));

            const fechaExpiracion = datos.exp * 1000;

            if (Date.now() >= fechaExpiracion) {
                cerrarSesion();
            }

        } catch (error) {
            cerrarSesion();
        }
    }

    onMount(() => {
        verificarSesion();

        // Comprueba la sesión cada segundo.
        const intervalo = setInterval(() => {
            verificarSesion();
        }, 1000);

        // Detecta cuando se cierra sesión desde otra pestaña.
        function escucharCambios(evento) {
            if (
                evento.key === 'token' ||
                evento.key === 'usuario'
            ) {
                verificarSesion();
            }
        }

        window.addEventListener('storage', escucharCambios);

        return () => {
            clearInterval(intervalo);
            window.removeEventListener('storage', escucharCambios);
        };
    });

    afterNavigate(() => {
        verificarSesion();
    });
</script>

<main class="content">
    <slot />
</main>

<style>
    :global(body) {
        margin: 0;
        padding: 0;
    }

    .content {
        min-height: 100vh;
        width: 100%;
    }
</style>

