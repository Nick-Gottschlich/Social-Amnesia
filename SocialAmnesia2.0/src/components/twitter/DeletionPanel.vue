<template>
  <div class="deletionContainer" v-if="loggedIn">
    <h1>Clean Twitter</h1>
    <div class="deletionButtonContainer">
      <b-button
        class="deletionButton"
        variant="danger"
        v-on:click="handleDeleteTweets()"
      >
        Click to delete tweets
      </b-button>
      <b-button variant="danger" v-on:click="handleDeleteFavorites()">
        Click to delete ❤️'s (favorites)
      </b-button>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-alert */
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";
import helpers from "@/util/helpers";

@Component
export default class DeletionPanel extends Vue {
  deleteItems(items, itemString, whitelistedItems) {
    const itemInSavedTimeRange = item => {
      const timeRangeObject = store.state.twitter[constants.TWITTER_TIME_RANGE];

      const hoursBackToSave =
        timeRangeObject.Hours +
        timeRangeObject.Days * 24 +
        timeRangeObject.Weeks * 168 +
        timeRangeObject.Years * 8766;
      const dateOfHoursBackToSave = new Date();
      dateOfHoursBackToSave.setHours(
        dateOfHoursBackToSave.getHours() - hoursBackToSave
      );

      return (
        new Date(item.created_at) >
        new Date(dateOfHoursBackToSave.toGMTString())
      );
    };

    const itemLowerThanScore = item => {
      if (
        item.favorite_count >=
        store.state.twitter[constants.TWITTER_FAVORITES_SCORE]
      ) {
        return false;
      }

      if (
        item.retweet_count >=
        store.state.twitter[constants.TWITTER_RETWEETS_SCORE]
      ) {
        return false;
      }

      return true;
    };

    if (
      window.confirm(
        `Are you sure you want to delete your ${itemString}? THIS ACTION IS PERMANENT!`
      )
    ) {
      const promiseArray = [];

      const shouldDeleteItem = item => {
        const itemIsWhitelisted = whitelistedItems[`${itemString}-${item.id}`];

        // add the "false" in here to skip deletion
        const shouldDelete =
          // false &&
          !itemIsWhitelisted &&
          (!itemInSavedTimeRange(item) ||
            !store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED]) &&
          (itemString === "favorites" ||
            itemLowerThanScore(item) ||
            !store.state.twitter[constants.TWITTER_SCORE_ENABLED]);

        return shouldDelete;
      };

      const totalItemsLength = items.filter(item => {
        return shouldDeleteItem(item);
      }).length;

      store.dispatch(constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED);
      store.dispatch(
        constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS,
        totalItemsLength
      );

      items.forEach(item => {
        if (shouldDeleteItem(item)) {
          promiseArray.push(
            store.state.twitter[constants.TWITTER_USER_CLIENT]
              .post(
                itemString === "tweets"
                  ? "statuses/destroy"
                  : "favorites/destroy",
                {
                  id: item.id_str
                }
              )
              .then(() => {
                store.commit(
                  constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED
                );
              })
              .catch(error => {
                console.log(
                  `Failed to delete item with error: ${JSON.stringify(error)}`
                );
              })
          );
        }
      });

      Promise.allSettled(promiseArray).then(() => {
        helpers.twitterGatherAndSetItems({
          apiRoute:
            itemString === "tweets"
              ? constants.TWEETS_ROUTE
              : constants.FAVORITES_ROUTE,
          itemArray: []
        });

        setTimeout(() => {
          store.dispatch(constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS, 0);
        }, 2500);
      });
    }
  }

  handleDeleteTweets() {
    this.deleteItems(
      store.state.twitter[constants.USER_TWEETS],
      "tweets",
      store.state.twitter[constants.WHITELISTED_TWEETS]
    );
  }

  handleDeleteFavorites() {
    this.deleteItems(
      store.state.twitter[constants.USER_FAVORITES],
      "favorites",
      store.state.twitter[constants.WHITELISTED_FAVORITES]
    );
  }

  get loggedIn() {
    return store.state.twitter[constants.TWITTER_LOGGED_IN];
  }
}
</script>

<style lang="scss">
.deletionContainer {
  border: 4mm ridge #dc3545;
  padding: 20px;
  margin-top: 10px;
}

.deletionButtonContainer {
  display: flex;
  flex-direction: column;
}

.deletionButton {
  margin-bottom: 5px;
}
</style>
