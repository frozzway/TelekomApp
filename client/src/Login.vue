<script>
import { defineComponent } from 'vue'
import AccountApi from './api/AccountApi'
import { setAccessToken } from "@/scripts/auth.js";

export default defineComponent({
  name: "Login",
  data() {
    return {
      form: {
        email: 'administrator@localhost.ru',
        password: 'qwerty123!',
        validCredentials: null
      }
    }
  },
  computed: {
    formFields() {
      return [this.form.email, this.form.password]
    }
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault()
      const response = await AccountApi.login(this.form.email, this.form.password)

      if (response.status === 401)
        this.form.validCredentials = false

      if (response.status === 200) {
        setAccessToken(response.data.access_token)
        await this.$router.push('/equipment')
      }
    }
  },
  watch: {
    formFields() {
      this.form.validCredentials = null
    }
  }
})
</script>

<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="p-4 border rounded shadow bg-white" style="width: 100%; max-width: 400px;">
      <BForm @submit="onSubmit">
        <div class="fs-4 mb-3 text-center">Вход в систему</div>
        <BFormGroup id="input-group-email" class="mb-3" :state="form.validCredentials">
          <BFormInput v-model="form.email" type="email" placeholder="Адрес электронной почты" required/>
        </BFormGroup>
        <BFormGroup id="input-group-password" class="mb-3" :state="form.validCredentials">
          <BFormInput v-model="form.password" type="password" placeholder="Пароль" required/>
          <BFormInvalidFeedback :state="form.validCredentials" class="">Данные для входа неверны</BFormInvalidFeedback>
        </BFormGroup>

        <div class="d-grid">
          <BButton type="submit" variant="primary">Войти</BButton>
        </div>
      </BForm>
    </div>
  </div>
</template>

<style scoped>

</style>