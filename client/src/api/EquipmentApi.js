import {apiClient} from "@/api/api-client.js";


/**
 * Класс для взаимодействия с сущностью "Оборудование"
 */
class EquipmentApi {
  static _controller = 'equipment'

  /**
   * Метод создания сущности
   * @param data объект передачи данных
   * @returns {Promise<object>}
   */
  static create = (data) => (
    apiClient.post(`/${this._controller}`, data)
  )

  /**
   * Метод получения сущности
   * @param id идентификатор сущности
   * @returns {Promise<object>}
   */
  static get = (id) => (
    apiClient(`/${this._controller}/${id}`)
  )

  /**
   * Метод получения таблицы сущности
   * @param params объект с фильтрами
   * @returns {Promise<object>}
   */
  static getGrid = (params) => (
    apiClient(`/${this._controller}`, { params: params })
  )

  /**
   * Метод редактирования сущности
   * @param id идентификатор сущности
   * @param data новые данные
   * @returns {Promise<object>}
   */
  static update = (id, data) => (
    apiClient.put(`/${this._controller}/${id}`, data)
  )

  /**
   * Метод удаления сущности
   * @param id идентификатор сущности
   * @returns {Promise}
   */
  static delete = (id) => (
    apiClient.delete(`/${this._controller}/${id}`)
  )
}

export default EquipmentApi