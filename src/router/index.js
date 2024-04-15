
import {createRouter, createWebHistory} from 'vue-router';
import JobApplication from '../components/JobApplication.vue';
import ApplicantsTable from '../components/ApplicantsTable.vue';
import LoginPage from '../components/LoginPage.vue';



const routes = [
  {
    path: '/',
    name: 'JobApplication',
    component: JobApplication
  },
  {
    path: '/login',
    component: LoginPage
  },
  {
    path: '/applicants',
    name: 'ApplicantsTable',
    component: ApplicantsTable,
    meta: { requiresAuth: true } 
  }
];
const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken') !== null || sessionStorage.getItem('authToken') !== null;
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); 
  } else {
    next();
  }
});

export default router;
