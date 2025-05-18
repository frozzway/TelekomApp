<script>
import { defineComponent } from 'vue'
import { isValidSerialNumber } from "@/scripts/utils.js"
import EquipmentApi from "@/api/EquipmentApi.js";
import EquipmentTypeApi from "@/api/EquipmentTypeApi.js";

export default defineComponent({
  name: "EditEquipmentForm",
  props: {
    entity_id: Number
  },
  data() {
    return {
      form: {
        equipment_type: null,
        serial_number: '',
        note: ''
      },
      equipment_types: [],
      wasSubmitted: false
    }
  },
  computed: {
    states_equipment_type() {
      if (!this.wasSubmitted) return null
      return this.form.equipment_type != null
    },
    states_serial_number() {
      if (!this.wasSubmitted) return null
      if (!this.states_equipment_type) {
        return false
      }

      return isValidSerialNumber(this.form.serial_number,
          this.form.equipment_type.serial_number_mask)
    }
  },
  methods: {
    async submit(event) {
      event.preventDefault()
      this.wasSubmitted = true
      if (!this.states_equipment_type || !this.states_serial_number) {
        return false
      }
      await EquipmentApi.update(this.$props.entity_id, {
        'note': this.form.note,
        'equipment_type_id': this.form.equipment_type.id,
        'serial_number': this.form.serial_number
      })
      return true
    }
  },
  async mounted() {
    const response = await EquipmentTypeApi.getList()
    this.equipment_types = response.data.map(item => ({
      value: item,
      text: `${item.name} (${item.serial_number_mask})`,
    }))

    const entity = await EquipmentApi.get(this.$props.entity_id)
    this.form.note = entity.note
    this.form.serial_number = entity.serial_number
    this.form.equipment_type = response.data.find(item => item.id === entity.equipment_type_id)
  }
})
</script>

<template>
  <BForm>
    <!-- Тип оборудования -->
    <BFormGroup label="Тип оборудования" :state="states_equipment_type">
      <BFormSelect
          v-model="form.equipment_type"
          :options="equipment_types"
          :state="states_equipment_type"
      />
      <BFormInvalidFeedback :state="states_equipment_type">
        Поле обязательно для заполнения
      </BFormInvalidFeedback>
    </BFormGroup>

    <!-- Серийный номер -->
    <BFormGroup label="Серийный номер" :state="states_serial_number">
      <BFormInput
          v-model="form.serial_number"
          :state="states_serial_number"
      />
      <BFormInvalidFeedback :state="states_serial_number">
        Поле не заполнено или не соответствует маске ввода
      </BFormInvalidFeedback>
    </BFormGroup>

    <!-- Примечание -->
    <BFormGroup label="Примечание">
      <BFormTextarea v-model="form.note"/>
    </BFormGroup>
  </BForm>
</template>

<style scoped>

</style>