import { createWebHistory, createRouter } from 'vue-router'
import Home from "@/Home.vue";
import Login from "@/Login.vue";

const routes = [
  { path: '/equipment', component: Home },
  { path: '/login', component: Login },
  { path: '/:pathMatch(.*)*', redirect: '/equipment' },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

export default router