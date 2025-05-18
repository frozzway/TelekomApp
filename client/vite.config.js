import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import Icons from 'unplugin-icons/vite'
import IconsResolve from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'
import {BootstrapVueNextResolver} from 'bootstrap-vue-next'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  const proxyEnabled = env.PROXY_REQUESTS === 'true'

  return {
    plugins: [
      vue(),
      vueDevTools(),
      Components({
        resolvers: [BootstrapVueNextResolver(), IconsResolve()],
        dts: true,
      }),
      Icons({
        compiler: 'vue3',
        autoInstall: true,
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      host: '0.0.0.0',
      ...(proxyEnabled && {
        proxy: {
          '/api': {
            target: 'http://localhost:5007/api',
            changeOrigin: true,
            rewrite: path => path.replace(/^\/api/, ''),
          },
        },
      }),
    }
  }
})
