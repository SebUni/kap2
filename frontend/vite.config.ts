import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    rollupOptions: {
      output: {
        // Aufteilung des Bundles (T-0122): ein einzelnes 3-MB-Bundle treibt den
        // Speicherbedarf des Baus und zwingt den Browser bei jeder Aenderung zum
        // vollstaendigen Neuladen. Gruppiert wird nach Bibliotheks-Familien.
        manualChunks(id: string) {
          if (!id.includes('node_modules')) return undefined
          const p = id.split('node_modules/').pop() ?? ''
          if (/^(@deck\.gl|@nebula\.gl|@luma\.gl|@loaders\.gl|@math\.gl|@probe\.gl)\//.test(p)) {
            return 'vendor-deckgl'
          }
          if (/^maplibre-gl\//.test(p)) return 'vendor-maplibre'
          if (/^(vis-network|vis-data|vis-util|@dagrejs)\//.test(p)) return 'vendor-vis'
          if (/^(recharts|d3-|victory-vendor|internmap|decimal\.js-light|fast-equals|es-toolkit|eventemitter3)/.test(p)) {
            return 'vendor-charts'
          }
          if (/^katex\//.test(p)) return 'vendor-katex'
          if (/^(react-markdown|remark-|rehype-|micromark|mdast-|hast-|unist-|unified|vfile|property-information|space-separated-tokens|comma-separated-tokens|html-url-attributes|bail|trough|devlop|zwitch|longest-streak|ccount|markdown-table|escape-string-regexp|character-entities|decode-named-character-reference|estree-util|is-plain-obj|trim-lines)/.test(p)) {
            return 'vendor-markdown'
          }
          if (/^@xyflow\//.test(p)) return 'vendor-xyflow'
          if (/^@tanstack\//.test(p)) return 'vendor-table'
          if (/^(react|react-dom|react-is|react-router|react-router-dom|scheduler|use-sync-external-store)\//.test(p)) {
            return 'vendor-react'
          }
          return 'vendor-misc'
        },
      },
    },
  },
  server: {
    port: 5173,
    hmr: {
      // Fix WebSocket connection failures in some network configs
      host: 'localhost',
      port: 5173,
      protocol: 'ws',
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
