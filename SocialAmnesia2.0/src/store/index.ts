import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    twitterLoggedIn: false,
    userTweets: [],
    userFavorites: []
  },
  mutations: {
    logInToTwitter(state) {
      state.twitterLoggedIn = true;
    },
    updateUserTweets(state, tweets) {
      state.userTweets = tweets;
    },
    updateUserFavorites(state, favorites) {
      state.userFavorites = favorites;
    }
  },
  actions: {
  },
  modules: {
  },
});
