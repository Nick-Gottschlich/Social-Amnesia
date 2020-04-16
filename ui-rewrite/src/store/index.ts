import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    twitterLoggedIn: false,
    userTweets: []
  },
  mutations: {
    logInToTwitter(state) {
      state.twitterLoggedIn = true;
    },
    updateUserTweets(state, tweets) {
      state.userTweets = tweets;
    }
  },
  actions: {
  },
  modules: {
  },
});
