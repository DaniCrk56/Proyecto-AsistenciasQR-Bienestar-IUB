<script>
    // Layout principal con el color institucional exacto del logo
</script>

<div class="app-container">
    <header class="main-header">
        <div class="logo-container">
            <!-- Asegúrate de que LogoIUB.png esté dentro de la carpeta static/ -->
            <img src="/LogoIUB.png" alt="Logo IUB" class="logo-img" />
            
            <div class="logo-fallback">IUB</div>
            
            <h1>Gestión de Eventos IUB</h1>
        </div>
    </header>

    <main class="content">
        <slot />
    </main>

    <footer>
        <p>Universidad de Barranquilla &bull; SvelteKit</p>
    </footer>
</div>

<style>
    .app-container {
        font-family: Arial, sans-serif;
        background-color: #f4f6f9;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        margin: 0;
    }
    .main-header {
        background-color: #121420; /* Color exacto extraído de fondo del logo */
        color: white;
        padding: 0.75rem 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        border-bottom: 2px solid #facc15; /* Un toque sutil con el amarillo institucional del punto del logo */
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .logo-img {
        height: 38px;
        width: auto;
        object-fit: contain;
    }
    .logo-fallback {
        background-color: #facc15;
        color: #121420;
        font-weight: bold;
        font-size: 0.8rem;
        padding: 0.4rem 0.6rem;
        border-radius: 4px;
        letter-spacing: 1px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.2rem;
        font-weight: bold;
        letter-spacing: 0.5px;
    }
    .content {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    footer {
        text-align: center;
        padding: 1rem;
        background-color: #e5e7eb;
        color: #4b5563;
        font-size: 0.85rem;
    }
</style>
