
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import adapter from '@sveltejs/adapter-node';

export default defineConfig({
    plugins: [
        sveltekit({
            adapter: adapter()
        })
    ],
    server: {
        proxy: {
            '/api': 'http://localhost:8000'
        }
    }
});
