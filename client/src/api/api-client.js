import axios from 'axios';
import { requestValidToken } from "@/scripts/auth.js";
import router from '@/scripts/router.js';

export const apiClient = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || ''}/api`,
  timeout: 5000,
})


class ControlledRedirect extends Error {}


apiClient.interceptors.request.use(
  async function (config) {
    if (config.skipAuth) return config;

    const accessToken = await requestValidToken();

    return {
        ...config,
        headers: {
            authorization: `Bearer ${accessToken}`
        }
    };
  }
)

apiClient.interceptors.response.use(
  function (response) {
    const { config, data } = response;
    return config.fullResponse ? response : data;
  },
  async function (error) {
    if (error instanceof ControlledRedirect) return Promise.resolve()

    const { response } = error;
    if (response) {
      const { status, data } = response;

      if (status === 401) {
        await router.push('/login');
        return Promise.reject(new ControlledRedirect())
      }

      const responseData = data?.error ?? data;

      alert(`Ошибка выполнения запроса: код: ${status}, ответ: ${responseData}`);
      return Promise.reject(response);
    }
    alert('Ошибка сети')
    return Promise.reject(error);
  })