import { createRouter, createWebHistory } from 'vue-router';
import MainMenu from '@/views/MainMenu.vue';
//import UploadForm from '@/views/UploadForm.vue';
import LoginPage from '@/views/LoginPage.vue';
import CsvEditorPage from '@/views/CsvEditorPage.vue';
import MetalCalculatePage from '@/views/MetalCalculatePage.vue';
import { isAuthenticated } from '@/utils/auth.js';

const routes = [
  { path: '/', name: 'MainMenu', component: MainMenu, meta: { requiresAuth: true } },
  { path: '/calculate', name: 'MetalCalculatePage', component: MetalCalculatePage, meta: { requiresAuth: true } },
  //{ path: '/calculate', name: 'UploadForm', component: UploadForm },
  { path: '/login', name: 'LoginPage', component: LoginPage },
  { path: '/csv', name: 'CsvEditor', component: CsvEditorPage, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next('/login');
  } else if (to.name === 'LoginPage' && isAuthenticated()) {
    next('/');
  } else {
    next();
  }
});

export default router;