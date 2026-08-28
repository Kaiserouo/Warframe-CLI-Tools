import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import svgr from "vite-plugin-svgr";

export default defineConfig(({ mode }) => {
  const isGithubPage = (mode === 'github');

  return {
    build: {
      outDir: isGithubPage ? 'build_github_page' : 'build',
    },

    base: isGithubPage ? '/Warframe-Tools/' : '/',

    plugins: [
      react(),
      tailwindcss(),
      svgr(),
    ],

    server: {   // tmp server proxy for backend API calls
      proxy: {
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
          secure: false,
        },
      },
    }
  };
});