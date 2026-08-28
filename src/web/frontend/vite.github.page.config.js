import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import svgr from "vite-plugin-svgr";
import { createHtmlPlugin } from 'vite-plugin-html'

export default defineConfig(() => {
  return {
    build: {
      outDir: 'build_github_page',
    },

    base: '/warframe-tools/',

    plugins: [
      react(),
      tailwindcss(),
      svgr(),
      createHtmlPlugin({
        template: 'index_github_page.html',
      })
    ],
  };
});