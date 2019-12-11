import Vue from 'vue';
import Router from 'vue-router';
import Drawer from '../components/Drawer.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/teddy',
      name: 'Teddy',
      component: Drawer,
    },
  ],
});
