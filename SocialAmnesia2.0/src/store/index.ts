import Vue from 'vue';
import Vuex from 'vuex';
import { LOGIN_TO_TWITTER, UPDATE_USER_TWEETS, UPDATE_USER_FAVORITES, UPDATE_USER_CLIENT } from './consts';

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
    logIntoTwitter(store) {
      store.commit(LOGIN_TO_TWITTER);
    },
    updateUserTweets(store, tweets) {
      store.commit(UPDATE_USER_TWEETS, tweets)
    },
    updateUserFavorites(store, favorites) {
      store.commit(UPDATE_USER_FAVORITES, favorites)
    },
    updateUserClient(store, client) {
      store.commit(UPDATE_USER_CLIENT, client)
    }
  },
  modules: {
  },
});
