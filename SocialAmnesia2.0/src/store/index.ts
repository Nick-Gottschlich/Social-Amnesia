import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    twitterLoggedIn: false,
    userTweets: [],
    userFavorites: [],
    twitterUserClient: {},
    whitelistedTweets: new Set(),
    whitelistedFavorites: new Set(),
  },
  mutations: {
    logIntoTwitter(state) {
      state.twitterLoggedIn = true;
    },
    updateUserTweets(state, tweets) {
      state.userTweets = tweets;
    },
    updateUserFavorites(state, favorites) {
      state.userFavorites = favorites;
    },
    updateUserClient(state, client) {
      state.twitterUserClient = client;
    }
  },
  actions: {
  },
  modules: {
  },
});
