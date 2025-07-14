import { createRouter, createWebHistory } from 'vue-router';
import MainMenu from '@/views/MainMenu.vue';
//import UploadForm from '@/views/UploadForm.vue';
import LoginPage from '@/views/LoginPage.vue';
import CsvEditorPage from '@/views/CsvEditorPage.vue';
import MetalCalculatePage from '@/views/MetalCalculatePage.vue';
import CalculationHistoryPage from '@/views/CalculationHistoryPage.vue';
import AdminDbView from '@/views/AdminDbView.vue';
import ItemDetailPage from '@/views/ItemDetailPage.vue';
import SpreadsheetDetailPage from '@/views/SpreadsheetDetailPage.vue';
import BoxGroupsPage from '@/views/BoxGroupsPage.vue';
import { isAuthenticated } from '@/utils/auth.js';

const routes = [
  { path: '/', name: 'MainMenu', component: MainMenu, meta: { requiresAuth: true } },
  { path: '/calculate', name: 'MetalCalculatePage', component: MetalCalculatePage, meta: { requiresAuth: true } },
  //{ path: '/calculate', name: 'UploadForm', component: UploadForm },
  { path: '/login', name: 'LoginPage', component: LoginPage },
  { path: '/csv', name: 'CsvEditor', component: CsvEditorPage, meta: { requiresAuth: true } },
  { path: '/history/box-groups', name: 'BoxGroups', component: BoxGroupsPage, meta: { requiresAuth: true } },
  { path: '/history/:historyId/item/:itemIndex', name: 'ItemDetail', component: ItemDetailPage, meta: { requiresAuth: true } },
  { path: '/history/:historyId/spreadsheet', name: 'SpreadsheetDetail', component: SpreadsheetDetailPage, meta: { requiresAuth: true } },
  { path: '/history', name: 'CalculationHistory', component: CalculationHistoryPage, meta: { requiresAuth: true } },
  { path: '/admin/db', name: 'AdminDbView', component: AdminDbView, meta: { requiresAuth: true, requiresAdmin: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  console.log('Router navigation:', { to: to.path, from: from.path })
  console.log('Requires auth:', to.meta.requiresAuth)
  console.log('Is authenticated:', isAuthenticated())
  
  if (to.meta.requiresAuth && !isAuthenticated()) {
    console.log('Redirecting to login - not authenticated')
    next('/login');
  } else if (to.name === 'LoginPage' && isAuthenticated()) {
    console.log('Redirecting to home - already authenticated')
    next('/');
  } else {
    console.log('Allowing navigation')
    next();
  }
});

export default router;