<script lang="ts">
import { defineComponent } from 'vue'
import EquipmentPage from "@/equipment/EquipmentPage.vue";

export default defineComponent({
  name: "Home",
  components: { EquipmentPage }
})
</script>

<template>
  <BContainer fluid="xl" class="mt-2">
    <EquipmentPage/>
  </BContainer>
</template>

<style scoped>

</style>