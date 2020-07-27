import Vue from "vue";
import VueRouter from "vue-router";
import Twitter from "@/views/Twitter.vue";
import About from "@/views/About.vue";
import Reddit from "@/views/Reddit.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "About",
    component: About
  },
  {
    path: "/twitter",
    name: "Twitter",
    component: Twitter
  },
  {
    path: "/reddit",
    name: "Reddit",
    component: Reddit
  }
];

// @ts-ignore
const router = new VueRouter({
  routes
});

export default router;
