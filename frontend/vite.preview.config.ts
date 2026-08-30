// Build-Konfiguration der Wirkungsmechanismus-Vorschau (Methodik-Workflow).
// Erzeugt ein einzelnes JS/CSS-Bundle (preview-dist/), das
// scripts/wirkungsmechanismus_preview.py in eine eigenständige HTML-Datei inlinet.
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
  base: './',
  build: {
    outDir: 'preview-dist',
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(__dirname, 'preview.html'),
      output: { inlineDynamicImports: true, manualChunks: undefined },
    },
    chunkSizeWarningLimit: 4000,
  },
})
