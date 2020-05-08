<template>
  <div class="deletionContainer" v-if="loggedIn">
    <h1>Clean Twitter</h1>
    <div class="deletionButtonContainer">
      <b-button
        class="deletionButton"
        variant="danger"
        v-on:click="handleDeleteTweets()"
      >Click to delete tweets</b-button>
      <b-button
        variant="danger"
        v-on:click="handleDeleteFavorites()"
      >Click to delete ❤️'s (favorites)</b-button>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-alert */
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";

@Component
export default class DeletionPanel extends Vue {
  deleteItems(items, itemString, whitelistedItems) {    
    if (
      window.confirm(
        `Are you sure you want to delete your ${itemString}? THIS ACTION IS PERMANENT!`
      )
    ) {
      store.dispatch(constants.RESET_CURRENTLY_DELETING_TOTAL_ITEMS);
      store.dispatch(constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS, items.length)
      items.forEach(tweet => {
        if (!whitelistedItems[`${itemString}-${tweet.id}`]) {
          store.state[constants.TWITTER_USER_CLIENT]
            .post(
              itemString === "tweets"
                ? "statuses/destroy"
                : "favorites/destroy",
              {
                id: tweet.id_str
              }
            )
            .then(() => {
              store.commit(constants.INCREMENT_CURRENTLY_DELETING_TOTAL_ITEMS);
            }).catch((error) => {
              console.log(`Failed to delete item with error: ${JSON.stringify(error)}`);
            });
        }
      });
    }
  }

  handleDeleteTweets() {
    this.deleteItems(
      store.state[constants.USER_TWEETS],
      "tweets",
      store.state[constants.WHITELISTED_TWEETS]
    );
  }

  handleDeleteFavorites() {
    this.deleteItems(
      store.state[constants.USER_FAVORITES],
      "favorites",
      store.state[constants.WHITELISTED_FAVORITES]
    );
  }

  get loggedIn() {
    return store.state[constants.TWITTER_LOGGED_IN];
  }
}
</script>

<style lang="scss">
.deletionContainer {
  border: 4mm ridge #dc3545;
  padding: 20px;
  margin-top: 10px;

  .deletionButtonContainer {
    display: flex;
    flex-direction: column;

    .deletionButton {
      margin-bottom: 5px;
    }
  }
}
</style>