/* eslint-disable no-param-reassign */
import Vue from 'vue';
import Vuex from 'vuex';
import Store from 'electron-store';
import constants from './constants';

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

// "middleware" to ensure that both the persistent store
//  and the vuex store are updated properly
const updateStore = (state, marker, value) => {
  state[marker] = value;
  persistentStore.set(marker, value)
}

export default new Vuex.Store({
  state: {
    twitterLoggedIn: persistentStore.get(constants.TWITTER_LOGGED_IN) || false,
    userTweets: persistentStore.get(constants.USER_TWEETS) || [],
    userFavorites: persistentStore.get(constants.USER_FAVORITES) || [],
    twitterUserClient: persistentStore.get(constants.TWITTER_USER_CLIENT) || {},
    whitelistedTweets: persistentStore.get(constants.WHITELISTED_TWEETS) || {},
    whitelistedFavorites: persistentStore.get(constants.WHITELISTED_FAVORITES) || {},
  },
  mutations: {
    logIntoTwitter(state) {
      updateStore(state, constants.TWITTER_LOGGED_IN, true);
    },
    updateUserTweets(state, tweets) {
      updateStore(state, constants.USER_TWEETS, tweets);
    },
    updateUserFavorites(state, favorites) {
      updateStore(state, constants.USER_FAVORITES, favorites);
    },
    updateUserClient(state, client) {
      updateStore(state, constants.TWITTER_USER_CLIENT, client);
    },
    updateWhitelistedTweets(state, tweetId) {
      addOrRemoveItem(state.whitelistedTweets, tweetId)
      persistentStore.set(constants.WHITELISTED_TWEETS, state.whitelistedTweets)
    },
    updateWhitelistedFavorites(state, tweetId) {
      addOrRemoveItem(state.whitelistedFavorites, tweetId)
      persistentStore.set(constants.WHITELISTED_FAVORITES, state.whitelistedFavorites)
    }
  },
  actions: {
    logIntoTwitter(store) {
      store.commit(constants.LOGIN_TO_TWITTER);
    },
    updateUserTweets(store, tweets) {
      store.commit(constants.UPDATE_USER_TWEETS, tweets)
    },
    updateUserFavorites(store, favorites) {
      store.commit(constants.UPDATE_USER_FAVORITES, favorites)
    },
    updateUserClient(store, client) {
      store.commit(constants.UPDATE_USER_CLIENT, client)
    },
    updateWhitelistedTweets(store, tweetId) {
      store.commit(constants.UPDATE_WHITELISTED_TWEETS, tweetId)
    },
    updateWhitelistedFavorites(store, favoriteId) {
      store.commit(constants.UPDATE_WHITELISTED_FAVORITES, favoriteId);
    }
  },
  modules: {
  },
});
