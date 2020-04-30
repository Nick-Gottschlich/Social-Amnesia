/* eslint-disable no-param-reassign */
import Vue from 'vue';
import Vuex from 'vuex';
import Store from 'electron-store';

import { LOGIN_TO_TWITTER, UPDATE_USER_TWEETS, UPDATE_USER_FAVORITES, UPDATE_USER_CLIENT, TWITTER_LOGGED_IN, USER_TWEETS, USER_FAVORITES, TWITTER_USER_CLIENT, WHITELISTED_TWEETS, WHITELISTED_FAVORITES, UPDATE_WHITELISTED_TWEETS, UPDATE_WHITELISTED_FAVORITES } from './consts';

Vue.use(Vuex);

const persistentStore = new Store();

// uncomment to manually clear persistent store
// persistentStore.clear()

const addOrRemoveItem = (whitelistedItems, itemId) => {
  if (whitelistedItems[itemId]) {
    whitelistedItems[itemId] = false;
  } else {
    whitelistedItems[itemId] = true;
  }
};

export default new Vuex.Store({
  state: {
    twitterLoggedIn: persistentStore.get(TWITTER_LOGGED_IN) || false,
    userTweets: persistentStore.get(USER_TWEETS) || [],
    userFavorites: persistentStore.get(USER_FAVORITES) || [],
    twitterUserClient: persistentStore.get(TWITTER_USER_CLIENT) || {},
    whitelistedTweets: persistentStore.get(WHITELISTED_TWEETS) || {},
    whitelistedFavorites: persistentStore.get(WHITELISTED_FAVORITES) || {},
  },
  mutations: {
    logIntoTwitter(state) {
      state.twitterLoggedIn = true;
      persistentStore.set(TWITTER_LOGGED_IN, true);
    },
    updateUserTweets(state, tweets) {
      state.userTweets = tweets;
      persistentStore.set(USER_TWEETS, tweets);
    },
    updateUserFavorites(state, favorites) {
      state.userFavorites = favorites;
      persistentStore.set(USER_FAVORITES, favorites);
    },
    updateUserClient(state, client) {
      state.twitterUserClient = client;
      persistentStore.set(TWITTER_USER_CLIENT, client);
    },
    updateWhitelistedTweets(state, tweetId) {
      addOrRemoveItem(state.whitelistedTweets, tweetId)
      persistentStore.set(WHITELISTED_TWEETS, state.whitelistedTweets)
    },
    updateWhitelistedFavorites(state, tweetId) {
      addOrRemoveItem(state.whitelistedFavorites, tweetId)
      persistentStore.set(WHITELISTED_FAVORITES, state.whitelistedFavorites)
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
    },
    updateWhitelistedTweets(store, tweetId) {
      store.commit(UPDATE_WHITELISTED_TWEETS, tweetId)
    },
    updateWhitelistedFavorites(store, favoriteId) {
      store.commit(UPDATE_WHITELISTED_FAVORITES, favoriteId);
    }
  },
  modules: {
  },
});
