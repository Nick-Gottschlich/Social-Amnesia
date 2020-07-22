/* eslint-disable no-param-reassign */
import Vue from "vue";
import Vuex from "vuex";
import Store from "electron-store";
// @ts-ignore
import Twitter from "twitter-lite";
import constants from "./constants";

Vue.use(Vuex);

interface TimeRangeModel {
  Hours: number;
  Days: number;
  Weeks: number;
  Years: number;
}

const REDDIT_CONSTANT = "reddit";
const TWITTER_CONSTANT = "twitter";

const twitterPersistentStore = new Store();
const redditPersistentStore = new Store();

// uncomment to manually clear persistent stores
// twitterPersistentStore.clear();
// redditPersistentStore.clear();

const addOrRemoveItem = (
  whitelistedItems: { [key: string]: boolean },
  itemId: string
) => {
  if (whitelistedItems[itemId]) {
    whitelistedItems[itemId] = false;
  } else {
    whitelistedItems[itemId] = true;
  }
};

// "middleware" to ensure that both the persistent store
//  and the vuex store are updated properly
const updateStore = (state: any, marker: string, value: any, site: string) => {
  state[site][marker] = value;
  if (site === TWITTER_CONSTANT) {
    twitterPersistentStore.set(marker, value);
  } else if (site === REDDIT_CONSTANT) {
    redditPersistentStore.set(marker, value);
  }
};

const twitterStoreDefault = {
  [constants.TWITTER_LOGGED_IN]: false,
  [constants.TWITTER_SCREEN_NAME]: "",
  [constants.TWITTER_USER_ID]: "",
  [constants.USER_TWEETS]: [],
  [constants.USER_FAVORITES]: [],
  [constants.TWITTER_USER_KEYS]: {},
  [constants.TWITTER_USER_CLIENT]: {},
  [constants.WHITELISTED_TWEETS]: {},
  [constants.WHITELISTED_FAVORITES]: {},
  [constants.TWITTER_TIME_RANGE_ENABLED]: false,
  [constants.TWITTER_TIME_RANGE]: {
    Hours: 0,
    Days: 0,
    Weeks: 0,
    Years: 0
  },
  [constants.TWITTER_SCORE_ENABLED]: false,
  [constants.TWITTER_FAVORITES_SCORE]: 0,
  [constants.TWITTER_RETWEETS_SCORE]: 0,
  [constants.TWITTER_SCHEDULE_DELETION_ENABLED]: {
    tweets: false,
    favorites: false
  },
  [constants.TWITTER_SCHEDULE_TIME]: ""
};

const redditStoreDefault = {
  [constants.REDDIT_LOGGED_IN]: false,
  [constants.REDDIT_USER_NAME]: "",
  [constants.REDDIT_ACCESS_TOKEN]: "",
  [constants.REDDIT_REFRESH_TOKEN]: "",
  [constants.REDDIT_COMMENTS]: [],
  [constants.REDDIT_POSTS]: [],
  [constants.REDDIT_WHITELISTED_COMMENTS]: {},
  [constants.REDDIT_WHITELISTED_POSTS]: {},
  [constants.REDDIT_TIME_RANGE_ENABLED]: false,
  [constants.REDDIT_TIME_RANGE]: {
    Hours: 0,
    Days: 0,
    Weeks: 0,
    Years: 0
  },
  [constants.REDDIT_SCORE_ENABLED]: false,
  [constants.REDDIT_UPVOTES_SCORE]: 0,
  [constants.REDDIT_SCHEDULE_DELETION_ENABLED]: {
    comments: false,
    posts: false
  },
  [constants.REDDIT_SCHEDULE_TIME]: ""
};

export default new Vuex.Store({
  state: {
    twitter: {
      [constants.TWITTER_LOGGED_IN]:
        twitterPersistentStore.get(constants.TWITTER_LOGGED_IN) || false,
      [constants.TWITTER_SCREEN_NAME]:
        twitterPersistentStore.get(constants.TWITTER_SCREEN_NAME) || "",
      [constants.TWITTER_USER_ID]:
        twitterPersistentStore.get(constants.TWITTER_USER_ID) || "",
      [constants.USER_TWEETS]:
        twitterPersistentStore.get(constants.USER_TWEETS) || [],
      [constants.USER_FAVORITES]:
        twitterPersistentStore.get(constants.USER_FAVORITES) || [],
      [constants.TWITTER_USER_KEYS]:
        twitterPersistentStore.get(constants.TWITTER_USER_KEYS) || {},
      [constants.TWITTER_USER_CLIENT]: twitterPersistentStore.get(
        constants.TWITTER_USER_CLIENT
      )
        ? new Twitter(twitterPersistentStore.get(constants.TWITTER_USER_KEYS))
        : {},
      [constants.WHITELISTED_TWEETS]:
        twitterPersistentStore.get(constants.WHITELISTED_TWEETS) || {},
      [constants.WHITELISTED_FAVORITES]:
        twitterPersistentStore.get(constants.WHITELISTED_FAVORITES) || {},
      [constants.TWITTER_TIME_RANGE_ENABLED]:
        twitterPersistentStore.get(constants.TWITTER_TIME_RANGE_ENABLED) ||
        false,
      [constants.TWITTER_TIME_RANGE]: twitterPersistentStore.get(
        constants.TWITTER_TIME_RANGE
      ) || {
        Hours: 0,
        Days: 0,
        Weeks: 0,
        Years: 0
      },
      [constants.TWITTER_SCORE_ENABLED]:
        twitterPersistentStore.get(constants.TWITTER_SCORE_ENABLED) || false,
      [constants.TWITTER_FAVORITES_SCORE]:
        twitterPersistentStore.get(constants.TWITTER_FAVORITES_SCORE) || 0,
      [constants.TWITTER_RETWEETS_SCORE]:
        twitterPersistentStore.get(constants.TWITTER_RETWEETS_SCORE) || 0,
      [constants.TWITTER_SCHEDULE_DELETION_ENABLED]: twitterPersistentStore.get(
        constants.TWITTER_SCHEDULE_DELETION_ENABLED
      ) || { tweets: false, favorites: false },
      [constants.TWITTER_SCHEDULE_TIME]:
        twitterPersistentStore.get(constants.TWITTER_SCHEDULE_TIME) || ""
    },
    reddit: {
      [constants.REDDIT_LOGGED_IN]:
        redditPersistentStore.get(constants.REDDIT_LOGGED_IN) || false,
      [constants.REDDIT_USER_NAME]:
        redditPersistentStore.get(constants.REDDIT_USER_NAME) || "",
      [constants.REDDIT_ACCESS_TOKEN]:
        redditPersistentStore.get(constants.REDDIT_ACCESS_TOKEN) || "",
      [constants.REDDIT_REFRESH_TOKEN]:
        redditPersistentStore.get(constants.REDDIT_REFRESH_TOKEN) || "",
      [constants.REDDIT_COMMENTS]:
        redditPersistentStore.get(constants.REDDIT_COMMENTS) || [],
      [constants.REDDIT_POSTS]:
        redditPersistentStore.get(constants.REDDIT_POSTS) || [],
      [constants.REDDIT_WHITELISTED_COMMENTS]:
        redditPersistentStore.get(constants.REDDIT_WHITELISTED_COMMENTS) || {},
      [constants.REDDIT_WHITELISTED_POSTS]:
        redditPersistentStore.get(constants.REDDIT_WHITELISTED_POSTS) || {},
      [constants.REDDIT_TIME_RANGE_ENABLED]:
        redditPersistentStore.get(constants.REDDIT_TIME_RANGE_ENABLED) || false,
      [constants.REDDIT_TIME_RANGE]: redditPersistentStore.get(
        constants.REDDIT_TIME_RANGE
      ) || {
        Hours: 0,
        Days: 0,
        Weeks: 0,
        Years: 0
      },
      [constants.REDDIT_SCORE_ENABLED]:
        redditPersistentStore.get(constants.REDDIT_SCORE_ENABLED) || false,
      [constants.REDDIT_UPVOTES_SCORE]:
        redditPersistentStore.get(constants.REDDIT_UPVOTES_SCORE) || 0,
      [constants.REDDIT_SCHEDULE_DELETION_ENABLED]: redditPersistentStore.get(
        constants.REDDIT_SCHEDULE_DELETION_ENABLED
      ) || { comments: false, posts: false },
      [constants.REDDIT_SCHEDULE_TIME]:
        redditPersistentStore.get(constants.REDDIT_SCHEDULE_TIME) || ""
    },
    [constants.CURRENTLY_DELETING]: {
      totalItems: 0,
      itemsDeleted: 0
    }
  },
  mutations: {
    [constants.LOGIN_TO_TWITTER](state) {
      updateStore(state, constants.TWITTER_LOGGED_IN, true, TWITTER_CONSTANT);
    },
    [constants.LOGOUT_OF_TWITTER](state) {
      Object.keys(state.twitter).forEach(key => {
        state.twitter[key] = twitterStoreDefault[key];
      });
      twitterPersistentStore.clear();
    },
    [constants.UPDATE_TWITTER_SCREEN_NAME](state, screenName) {
      updateStore(
        state,
        constants.TWITTER_SCREEN_NAME,
        screenName,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_TWITTER_USER_ID](state, userId) {
      updateStore(state, constants.TWITTER_USER_ID, userId, TWITTER_CONSTANT);
    },
    [constants.UPDATE_USER_TWEETS](state, tweets) {
      updateStore(state, constants.USER_TWEETS, tweets, TWITTER_CONSTANT);
    },
    [constants.UPDATE_USER_FAVORITES](state, favorites) {
      updateStore(state, constants.USER_FAVORITES, favorites, TWITTER_CONSTANT);
    },
    [constants.UPDATE_TWITTER_USER_KEYS](state, keys) {
      updateStore(state, constants.TWITTER_USER_KEYS, keys, TWITTER_CONSTANT);
    },
    [constants.UPDATE_TWITTER_USER_CLIENT](state, client) {
      updateStore(
        state,
        constants.TWITTER_USER_CLIENT,
        client,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_WHITELISTED_TWEETS](state, tweetId) {
      addOrRemoveItem(state.twitter[constants.WHITELISTED_TWEETS], tweetId);
      twitterPersistentStore.set(
        constants.WHITELISTED_TWEETS,
        state.twitter[constants.WHITELISTED_TWEETS]
      );
    },
    [constants.UPDATE_WHITELISTED_FAVORITES](state, favoriteId) {
      addOrRemoveItem(
        state.twitter[constants.WHITELISTED_FAVORITES],
        favoriteId
      );
      twitterPersistentStore.set(
        constants.WHITELISTED_FAVORITES,
        state.twitter[constants.WHITELISTED_FAVORITES]
      );
    },
    [constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED](state) {
      // @ts-ignore
      state[constants.CURRENTLY_DELETING].itemsDeleted += 1;
    },
    [constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED](state) {
      state[constants.CURRENTLY_DELETING].itemsDeleted = 0;
    },
    [constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS](state, totalItems) {
      state[constants.CURRENTLY_DELETING].totalItems = totalItems;
    },
    [constants.UPDATE_TWITTER_TIME_RANGE_ENABLED](state, enabled) {
      updateStore(
        state,
        constants.TWITTER_TIME_RANGE_ENABLED,
        enabled,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_TWITTER_TIME_RANGE](state, timeRange: TimeRangeModel) {
      updateStore(
        state,
        constants.TWITTER_TIME_RANGE,
        timeRange,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_TWITTER_SCORE_ENABLED](state, enabled: boolean) {
      updateStore(
        state,
        constants.TWITTER_SCORE_ENABLED,
        enabled,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_TWITTER_FAVORITES_SCORE](state, score: number) {
      updateStore(
        state,
        constants.TWITTER_FAVORITES_SCORE,
        score,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_TWITTER_RETWEETS_SCORE](state, score: number) {
      updateStore(
        state,
        constants.TWITTER_RETWEETS_SCORE,
        score,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_TWITTER_SCHEDULE_DELETION_ENABLED](state, enabledObject) {
      updateStore(
        state,
        constants.TWITTER_SCHEDULE_DELETION_ENABLED,
        enabledObject,
        TWITTER_CONSTANT
      );
    },
    [constants.UPDATE_TWITTER_SCHEDULE_TIME](state, time) {
      updateStore(
        state,
        constants.TWITTER_SCHEDULE_TIME,
        time,
        TWITTER_CONSTANT
      );
    },
    [constants.LOGIN_TO_REDDIT](state) {
      updateStore(state, constants.REDDIT_LOGGED_IN, true, REDDIT_CONSTANT);
    },
    [constants.LOGOUT_OF_REDDIT](state) {
      Object.keys(state.reddit).forEach(key => {
        state.reddit[key] = redditStoreDefault[key];
      });
      redditPersistentStore.clear();
    },
    [constants.UPDATE_REDDIT_USER_NAME](state, screenName) {
      updateStore(
        state,
        constants.REDDIT_USER_NAME,
        screenName,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_ACCESS_TOKEN](state, accessToken) {
      updateStore(
        state,
        constants.REDDIT_ACCESS_TOKEN,
        accessToken,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_REFRESH_TOKEN](state, refreshToken) {
      updateStore(
        state,
        constants.REDDIT_REFRESH_TOKEN,
        refreshToken,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_COMMENTS](state, comments) {
      updateStore(state, constants.REDDIT_COMMENTS, comments, REDDIT_CONSTANT);
    },
    [constants.UPDATE_REDDIT_POSTS](state, posts) {
      updateStore(state, constants.REDDIT_POSTS, posts, REDDIT_CONSTANT);
    },
    [constants.UPDATE_REDDIT_WHITELISTED_COMMENTS](state, commentId) {
      addOrRemoveItem(
        state.reddit[constants.REDDIT_WHITELISTED_COMMENTS],
        commentId
      );
      redditPersistentStore.set(
        constants.REDDIT_WHITELISTED_COMMENTS,
        state.reddit[constants.REDDIT_WHITELISTED_COMMENTS]
      );
    },
    [constants.UPDATE_REDDIT_WHITELISTED_POSTS](state, postId) {
      addOrRemoveItem(state.reddit[constants.REDDIT_WHITELISTED_POSTS], postId);
      redditPersistentStore.set(
        constants.REDDIT_WHITELISTED_POSTS,
        state.reddit[constants.REDDIT_WHITELISTED_POSTS]
      );
    },
    [constants.UPDATE_REDDIT_TIME_RANGE_ENABLED](state, enabled) {
      updateStore(
        state,
        constants.REDDIT_TIME_RANGE_ENABLED,
        enabled,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_TIME_RANGE](state, timeRange: TimeRangeModel) {
      updateStore(
        state,
        constants.REDDIT_TIME_RANGE,
        timeRange,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_SCORE_ENABLED](state, enabled: boolean) {
      updateStore(
        state,
        constants.REDDIT_SCORE_ENABLED,
        enabled,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_UPVOTES_SCORE](state, score: number) {
      updateStore(
        state,
        constants.REDDIT_UPVOTES_SCORE,
        score,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_SCHEDULE_DELETION_ENABLED](state, enabledObject) {
      updateStore(
        state,
        constants.REDDIT_SCHEDULE_DELETION_ENABLED,
        enabledObject,
        REDDIT_CONSTANT
      );
    },
    [constants.UPDATE_REDDIT_SCHEDULE_TIME](state, time) {
      updateStore(state, constants.REDDIT_SCHEDULE_TIME, time, REDDIT_CONSTANT);
    }
  },
  actions: {
    [constants.LOGIN_TO_TWITTER](store) {
      store.commit(constants.LOGIN_TO_TWITTER);
    },
    [constants.LOGOUT_OF_TWITTER](store) {
      store.commit(constants.LOGOUT_OF_TWITTER);
    },
    [constants.UPDATE_TWITTER_SCREEN_NAME](store, screenName) {
      store.commit(constants.UPDATE_TWITTER_SCREEN_NAME, screenName);
    },
    [constants.UPDATE_TWITTER_USER_ID](store, userId) {
      store.commit(constants.UPDATE_TWITTER_USER_ID, userId);
    },
    [constants.UPDATE_USER_TWEETS](store, tweets) {
      store.commit(constants.UPDATE_USER_TWEETS, tweets);
    },
    [constants.UPDATE_USER_FAVORITES](store, favorites) {
      store.commit(constants.UPDATE_USER_FAVORITES, favorites);
    },
    [constants.UPDATE_TWITTER_USER_KEYS](store, keys) {
      store.commit(constants.UPDATE_TWITTER_USER_KEYS, keys);
    },
    [constants.UPDATE_TWITTER_USER_CLIENT](store, client) {
      store.commit(constants.UPDATE_TWITTER_USER_CLIENT, client);
    },
    [constants.UPDATE_WHITELISTED_TWEETS](store, tweetId) {
      store.commit(constants.UPDATE_WHITELISTED_TWEETS, tweetId);
    },
    [constants.UPDATE_WHITELISTED_FAVORITES](store, favoriteId) {
      store.commit(constants.UPDATE_WHITELISTED_FAVORITES, favoriteId);
    },
    [constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED](store) {
      store.commit(constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED);
    },
    [constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED](store) {
      store.commit(constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED);
    },
    [constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS](store, totalItems) {
      store.commit(constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS, totalItems);
    },
    [constants.UPDATE_TWITTER_TIME_RANGE_ENABLED](store, enabled) {
      store.commit(constants.UPDATE_TWITTER_TIME_RANGE_ENABLED, enabled);
    },
    [constants.UPDATE_TWITTER_TIME_RANGE](store, timeRange: TimeRangeModel) {
      store.commit(constants.UPDATE_TWITTER_TIME_RANGE, timeRange);
    },
    [constants.UPDATE_TWITTER_SCORE_ENABLED](store, enabled: boolean) {
      store.commit(constants.UPDATE_TWITTER_SCORE_ENABLED, enabled);
    },
    [constants.UPDATE_TWITTER_FAVORITES_SCORE](store, score: number) {
      store.commit(constants.UPDATE_TWITTER_FAVORITES_SCORE, score);
    },
    [constants.UPDATE_TWITTER_RETWEETS_SCORE](store, score: number) {
      store.commit(constants.UPDATE_TWITTER_RETWEETS_SCORE, score);
    },
    [constants.UPDATE_TWITTER_SCHEDULE_DELETION_ENABLED](store, enabledObject) {
      store.commit(
        constants.UPDATE_TWITTER_SCHEDULE_DELETION_ENABLED,
        enabledObject
      );
    },
    [constants.UPDATE_TWITTER_SCHEDULE_TIME](store, time) {
      store.commit(constants.UPDATE_TWITTER_SCHEDULE_TIME, time);
    },
    [constants.LOGIN_TO_REDDIT](store) {
      store.commit(constants.LOGIN_TO_REDDIT);
    },
    [constants.LOGOUT_OF_REDDIT](store) {
      store.commit(constants.LOGOUT_OF_REDDIT);
    },
    [constants.UPDATE_REDDIT_USER_NAME](store, screenName) {
      store.commit(constants.UPDATE_REDDIT_USER_NAME, screenName);
    },
    [constants.UPDATE_REDDIT_ACCESS_TOKEN](store, accessToken) {
      store.commit(constants.UPDATE_REDDIT_ACCESS_TOKEN, accessToken);
    },
    [constants.UPDATE_REDDIT_REFRESH_TOKEN](store, refreshToken) {
      store.commit(constants.UPDATE_REDDIT_REFRESH_TOKEN, refreshToken);
    },
    [constants.UPDATE_REDDIT_COMMENTS](store, comments) {
      store.commit(constants.UPDATE_REDDIT_COMMENTS, comments);
    },
    [constants.UPDATE_REDDIT_POSTS](store, posts) {
      store.commit(constants.UPDATE_REDDIT_POSTS, posts);
    },
    [constants.UPDATE_REDDIT_WHITELISTED_COMMENTS](store, commentId) {
      store.commit(constants.UPDATE_REDDIT_WHITELISTED_COMMENTS, commentId);
    },
    [constants.UPDATE_REDDIT_WHITELISTED_POSTS](store, postId) {
      store.commit(constants.UPDATE_REDDIT_WHITELISTED_POSTS, postId);
    },
    [constants.UPDATE_REDDIT_TIME_RANGE_ENABLED](store, enabled) {
      store.commit(constants.UPDATE_REDDIT_TIME_RANGE_ENABLED, enabled);
    },
    [constants.UPDATE_REDDIT_TIME_RANGE](store, timeRange: TimeRangeModel) {
      store.commit(constants.UPDATE_REDDIT_TIME_RANGE, timeRange);
    },
    [constants.UPDATE_REDDIT_SCORE_ENABLED](store, enabled: boolean) {
      store.commit(constants.UPDATE_REDDIT_SCORE_ENABLED, enabled);
    },
    [constants.UPDATE_REDDIT_UPVOTES_SCORE](store, score: number) {
      store.commit(constants.UPDATE_REDDIT_UPVOTES_SCORE, score);
    },
    [constants.UPDATE_REDDIT_SCHEDULE_DELETION_ENABLED](store, enabledObject) {
      store.commit(
        constants.UPDATE_REDDIT_SCHEDULE_DELETION_ENABLED,
        enabledObject
      );
    },
    [constants.UPDATE_REDDIT_SCHEDULE_TIME](store, time) {
      store.commit(constants.UPDATE_REDDIT_SCHEDULE_TIME, time);
    }
  },
  modules: {}
});
