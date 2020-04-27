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

@Component
export default class DeletionPanel extends Vue {
  deleteItems(items, itemString, whitelistedItems) {
    if (window.confirm(`Are you sure you want to delete your ${itemString}?`)) {
      items.forEach(tweet => {
        if (!whitelistedItems.has(`${itemString}-${tweet.id}`)) {
          store.state.twitterUserClient.post(
            itemString === "tweets" ? "statuses/destroy" : "favorites/destroy",
            {
              id: tweet.id_str
            }
          );
        }
      });
    }
  }

  handleDeleteTweets() {
    this.deleteItems(
      store.state.userTweets,
      "tweets",
      store.state.whitelistedTweets
    );
  }

  handleDeleteFavorites() {
    this.deleteItems(
      store.state.userFavorites,
      "favorites",
      store.state.whitelistedFavorites
    );
  }

  get loggedIn() {
    return store.state.twitterLoggedIn;
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