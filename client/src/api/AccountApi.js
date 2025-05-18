import { apiClient } from "@/api/api-client.js";

/**
 * @typedef {Object} AuthTokens
 * @property {string} access_token - Токен доступа.
 * @property {string} refresh_token - Токен обновления.
 */

/**
 * Класс для работы с авторизацией
 */
class AccountApi {
  static _controller = 'account'

  /**
   * Метод авторизации
   * @param username email пользователя
   * @param password пароль пользователя
     @returns {Promise<AuthTokens>}
   */
  static login = (username, password) => (
    apiClient(`/${this._controller}/login`,
      {
        skipAuth: true,
        method: 'post',
        data: {
          username: username,
          password: password,
        },
        fullResponse: true,
        validateStatus: (status) => status >= 200 && status < 500,
      })
  )

  /**
   * Метод обновления сессии и получения свежего Access токена
   * @returns {Promise<AuthTokens>}
   */
  static refreshToken = () => (
    apiClient(`/${this._controller}/refresh_session`, { skipAuth: true })
  )

  /**
   * Метод выхода из системы
   * @returns {Promise<null>}
   */
  static logout = () => (
    apiClient(`/${this._controller}/logout`,
      {
        skipAuth: true,
        method: 'post',
      })
  )
}

export default AccountApi