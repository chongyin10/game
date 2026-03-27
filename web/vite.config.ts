import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3333,
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5002',
        changeOrigin: true,
        // 允许跨域携带 cookie
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req) => {
            // 转发 cookie
            if (req.headers.cookie) {
              proxyReq.setHeader('Cookie', req.headers.cookie)
            }
          })
          proxy.on('proxyRes', (proxyRes, req, res) => {
            // 转发后端设置的 cookie 到前端
            const cookies = proxyRes.headers['set-cookie']
            if (cookies) {
              res.setHeader('Set-Cookie', cookies)
            }
          })
        },
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          utils: ['axios'],
        },
      },
    },
  },
})
