
<script>
    import { afterNavigate } from '$app/navigation';

    afterNavigate(() => {
        const ruta = window.location.pathname;

        const token = localStorage.getItem('token');
        const usuario = localStorage.getItem('usuario');

       if (ruta !== '/' && ruta !== '/registro' && (!token || !usuario)) {
            window.location.replace('/');
        }
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
