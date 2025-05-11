import axios from 'axios';

export const apiClient = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || ''}/api`,
  timeout: 5000,
})


apiClient.interceptors.response.use(
  function (response) {
    const { config, data } = response;
    return config.fullResponse ? response : data;
  },
  function (error) {
    const { request, response, config } = error;
    if (response) {
      const { status, data } = response;
      alert(`Ошибка выполнения запроса: код: ${status}, ответ: ${data}`);
      return Promise.reject(response);
    }
    alert('Ошибка сети')
    return Promise.reject(error);
  })