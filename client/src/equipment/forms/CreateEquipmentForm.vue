<script>
import { defineComponent } from 'vue'
import { BForm, BFormInvalidFeedback, BFormTextarea } from "bootstrap-vue-next";
import EquipmentApi from "@/api/EquipmentApi.js";
import EquipmentTypeApi from "@/api/EquipmentTypeApi.js";
import { filterInvalidSerialNumbers } from "@/scripts/utils.js"


export default defineComponent({
  name: "CreateEquipmentForm",
  components: {BForm, BFormTextarea, BFormInvalidFeedback},
  data() {
    return {
      form: {
        equipment_type: null,
        serial_numbers: '',
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
    states_serial_numbers() {
      if (!this.wasSubmitted) return null
      if (!this.states_equipment_type || this.serial_numbers().length < 1) {
        return false
      }

      const invalidSerialNumbers = filterInvalidSerialNumbers(this.serial_numbers(),
          this.form.equipment_type.serial_number_mask)

      return invalidSerialNumbers.length === 0
    }
  },
  methods: {
    serial_numbers() {
      return this.form.serial_numbers
          .split(',')
          .map(item => item.trim())
          .filter(item => item !== '');
    },
    async submit(event) {
      event.preventDefault()
      this.wasSubmitted = true
      if (!this.states_equipment_type || !this.states_serial_numbers) {
        return false
      }
      await EquipmentApi.create({
        'note': this.form.note,
        'equipment_type_id': this.form.equipment_type.id,
        'serial_numbers': this.serial_numbers()
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

    <!-- Серийные номера -->
    <BFormGroup label="Серийные номера" :state="states_serial_numbers">
      <BFormTextarea
          v-model="form.serial_numbers"
          :state="states_serial_numbers"
      />
      <BFormInvalidFeedback :state="states_serial_numbers">
        Поле не заполнено или не соответствует маске ввода
      </BFormInvalidFeedback>
    </BFormGroup>

    <!-- Примечание -->
    <BFormGroup label="Примечание">
      <BFormTextarea
          v-model="form.note"
      />
    </BFormGroup>
  </BForm>
</template>

<style scoped>

</style>