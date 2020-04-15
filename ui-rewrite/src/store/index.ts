import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    twitterLoggedIn: false
  },
  mutations: {
    logInToTwitter(state) {
      console.log('loggin in to twitter!')
      state.twitterLoggedIn = true;
    }
  },
  actions: {
  },
  modules: {
  },
});
