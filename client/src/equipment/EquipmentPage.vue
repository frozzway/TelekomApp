<script>
import {defineComponent} from 'vue'
import {
  BButton,
  BCol,
  BContainer,
  BFormGroup, BFormInput, BFormRadioGroup,
  BFormSelect, BInput,
  BModal,
  BPagination,
  BRow,
  BTable
} from "bootstrap-vue-next";

import CreateEquipmentForm from "@/equipment/forms/CreateEquipmentForm.vue";
import EditEquipmentForm from "@/equipment/forms/EditEquipmentForm.vue";
import EquipmentApi from "@/api/EquipmentApi.js";
import AccountApi from "@/api/AccountApi.js";
import { removeAccessToken } from "@/scripts/auth.js";


export default defineComponent({
  name: "EquipmentPage",
  components: {
    EditEquipmentForm,
    BFormRadioGroup,
    BFormInput, BInput, BModal, BButton, BCol, BRow, BFormGroup, BContainer, BTable, BPagination, BFormSelect,
    CreateEquipmentForm
  },
  data() {
    return {
      perPage: 10,
      currentPage: 1,
      totalRows: 0,
      isBusy: false,
      filterOptions: [
        {text: 'Примечание', value: 'note'},
        {text: 'S/N', value: 'serial_number'}
      ],
      filterSelected: 'serial_number',
      filterValue: '',
      typingTimer: null,
      fields: [
        {
          key: 'edit-action',
          label: '',
          thClass: 'icon-column',
          tdClass: 'text-center'
        },
          'id',
        {
          'key': 'serial_number',
          label: 'S/N'
        },
        {
          'key': 'equipment_type_name',
          'label': 'Тип оборудования'
        },
        {
          key: 'note',
          label: 'Примечание',
          tdClass: 'text-column'
        },
        {
          key: 'delete-action',
          label: '',
          thClass: 'icon-column',
          tdClass: 'text-center align-middle'
        }],
      cacheData: {},
      tableKey: 0,
      pageOptions: [
        {value: 10, text: '10'},
        {value: 25, text: '25'},
        {value: 50, text: '50'},
        {value: 100, text: '100'}
      ],
      createModal: {
        show: false,
        init_form: false,
      },
      editModal: {
        id: 0,
        show: false,
        init_form: false,
      }
    }
  },
  methods: {
    async provider(ctx) {
      this.isBusy = true
      const {perPage, currentPage} = ctx
      const key = `${perPage}:${currentPage}`

      if (this.cacheData[key]) {
        this.isBusy = false
        return this.cacheData[key]
      }

      let {data: pageData, total_count} = await this.getData(currentPage, perPage)

      if (pageData.length === 0 && total_count > 0) {
        this.currentPage = Math.ceil(total_count / perPage)
        const response = await this.getData(this.currentPage, perPage)
        total_count = response.total_count
        pageData = response.data
      }

      this.totalRows = total_count
      this.isBusy = false

      return pageData
    },
    async getData(currentPage, perPage) {
      const skip = (currentPage - 1) * perPage
      const params = {
        require_total_count: true,
        skip: skip,
        take: perPage
      }
      if (this.filterValue) {
        params[this.filterSelected] = this.filterValue
      }
      const response = await EquipmentApi.getGrid(params)
      this.cacheData[`${perPage}:${currentPage}`] = response.data
      return response
    },
    refresh() {
      this.cacheData = {}
      this.tableKey++
    },
    onPerPageChange(value) {
      const oldPage = this.currentPage
      this.perPage = value
      setTimeout(() => this.currentPage = oldPage)
    },
    async onCreateModelOk(event) {
      const success = await this.$refs["create-form-modal"].submit(event)
      if (success) {
        this.createModal.show = false
        this.refresh()
      }
    },
    async onEditModelOk(event) {
      const success = await this.$refs["edit-form-modal"].submit(event)
      if (success) {
        this.editModal.show = false
        this.refresh()
      }
    },
    openCreateForm() {
      this.createModal.show = true
      this.createModal.init_form = true
    },
    openEditForm(item) {
      this.editModal.id = item.id
      this.editModal.show = true
      this.editModal.init_form = true
    },
    async deleteRow(item) {
      await EquipmentApi.delete(item.id)
      this.refresh()
      alert('Успешно удалено')
    },
    async logout() {
      await AccountApi.logout()
      removeAccessToken()
      await this.$router.push('/login')
    }
  },
  watch: {
    filterValue(newVal) {
      clearTimeout(this.typingTimer)
      // Запустим refresh через 500 мс после последнего ввода
      this.typingTimer = setTimeout(() => {
        this.refresh()
      }, 500)
    },
    filterSelected(newVal) {
      if (this.filterValue) this.refresh()
    }
  }
})
</script>

<template>
  <!-- Модальные окна -->
  <BModal
      v-model="createModal.show"
      title="Добавить запись"
      @hidden="createModal.init_form = false"
      @ok="onCreateModelOk"
      ok-title="Создать"
      cancel-title="Отмена"
      no-close-on-backdrop
  >
    <CreateEquipmentForm v-if="createModal.init_form" ref="create-form-modal"/>
  </BModal>
  <BModal
      v-model="editModal.show"
      title="Редактировать запись"
      @hidden="editModal.init_form = false"
      @ok="onEditModelOk"
      ok-title="Сохранить"
      cancel-title="Отмена"
      no-close-on-backdrop
  >
    <EditEquipmentForm v-if="editModal.init_form" :entity_id="editModal.id" ref="edit-form-modal"/>
  </BModal>

  <!-- Верхняя панель с кнопками -->
  <BRow class="mb-2" align-v="center">
    <BCol>
      Управление: <h5>Оборудование</h5>
    </BCol>
    <BCol>
      <BRow align-h="end">
        <BCol cols="auto">
          <BButton variant="outline-secondary" @click="logout()">Выйти</BButton>
        </BCol>
      </BRow>
    </BCol>
  </BRow>
  <BRow>
    <BCol cols="12" md="auto">
      <BButton variant="primary" @click="openCreateForm()">
        Добавить
      </BButton>
    </BCol>

    <BCol>
      <BRow align-v="center" align-h="end">
        <BCol cols="auto">
          <BFormRadioGroup v-model="filterSelected" :options="filterOptions" name="radio-inline"/>
        </BCol>
        <BCol cols="auto">
          <BFormInput placeholder="Поиск" v-model="filterValue"></BFormInput>
        </BCol>
        <BCol cols="auto">
          <BButton variant="secondary" @click="refresh">
            <IMaterialSymbolsRefresh class=""/>
          </BButton>
        </BCol>
      </BRow>
    </BCol>
  </BRow>

  <!-- Таблица -->
  <BTable
      :key="tableKey"
      striped
      hover
      responsive="true"
      class="mt-2 overflow-x-auto"
      :provider="provider"
      :fields="fields"
      :busy="isBusy"
      :per-page="perPage"
      :current-page="currentPage"
      :bordered="true"
  >
    <template #cell(edit-action)="row">
      <BButton variant="link" class="icon-btn" size="lg">
        <IMaterialSymbolsEditRounded color="blue" @click="openEditForm(row.item)"/>
      </BButton>
    </template>
    <template #cell(delete-action)="row">
      <BButton variant="link" class="icon-btn" size="lg" @click="deleteRow(row.item)">
        <IMaterialSymbolsDeleteOutlineSharp color="red"/>
      </BButton>
    </template>
  </BTable>

  <!-- Нижняя панель с кнопками -->
  <BRow align-v="center">
    <BCol>
      <BPagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="start"
          class="mb-0"
      />
    </BCol>
    <BCol>
      <BRow align-v="center" align-h="end">
        <BCol cols="auto">
          <label class="form-label mb-0 d-none d-md-block">Отображать на странице</label>
        </BCol>
        <BCol cols="auto">
          <BFormSelect
              id="per-page-select"
              :model-value="perPage"
              @update:model-value="onPerPageChange"
              :options="pageOptions"
          />
        </BCol>
      </BRow>
    </BCol>
  </BRow>
</template>

<style scoped>
.icon-btn {
  padding: 0;
  width: auto;
  height: auto;
  min-width: 0;
  line-height: 1;
}

::v-deep(.icon-column) {
  width: 50px;
}

::v-deep(.text-column) {
  word-break: break-word;
  min-width: 120px;
}
</style>