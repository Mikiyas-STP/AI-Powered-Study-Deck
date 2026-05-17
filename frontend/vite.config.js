import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    // This is the fix for the "Blocked request" error
    allowedHosts: true, 
    host: true, // Ensures Vite listens on all local IPs inside the container
    port: 5173,
  }

})
