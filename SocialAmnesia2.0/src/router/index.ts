import Vue from 'vue';
import VueRouter from 'vue-router';
import Twitter from '@/views/Twitter.vue';
import About from '@/views/About.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'About',
    component: About,
  },
  {
    path: '/twitter',
    name: 'Twitter',
    component: Twitter
  },
];

const router = new VueRouter({
  routes,
});

export default router;
