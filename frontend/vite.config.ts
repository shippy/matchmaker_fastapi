import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // set up server and HMR ports to work within a Docker container
  server: {
    host: "0.0.0.0",
    port: 5173,
    hmr: {
      port: 5174
    },
    watch: {
      usePolling: true
    }
  }
})
