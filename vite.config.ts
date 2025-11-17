import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteMockServe } from 'vite-plugin-mock'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  // command: 'serve' | 'build'
  // mode: 'development' | 'production'
  const isDev = command === 'serve' || mode === 'development'

  return {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },
    plugins: [
      vue(),
      viteMockServe({
        mockPath: 'src/mock',
        enable: isDev, // 仅在开发环境启用 mock
        watchFiles: true,
        localEnabled: isDev,
        prodEnabled: false
      })
    ]
  }
})
