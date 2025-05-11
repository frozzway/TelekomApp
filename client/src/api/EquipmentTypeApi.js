import {apiClient} from "@/api/api-client.js";


class EquipmentTypeApi {
  static _controller = 'equipment-type'

  /**
   * Метод получения списка сущностей "Тип оборудования"
   * @returns {Promise<object>}
   */
  static getList = () => (
    apiClient(`/${this._controller}`)
  )
}

export default EquipmentTypeApi