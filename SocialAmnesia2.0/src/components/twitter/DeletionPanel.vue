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
  handleDeleteTweets() {
    if (window.confirm("Are you sure you want to delete your tweets?")) {
      store.state.userTweets.forEach(tweet => {
        store.state.twitterUserClient.post("statuses/destroy", {
          id: tweet.id_str
        });
      });
    }
  }

  handleDeleteFavorites() {
    if (window.confirm("Are you sure you want to delete your favorites?")) {
      store.state.userFavorites.forEach(tweet => {
        store.state.twitterUserClient.post("favorites/destroy", {
          id: tweet.id_str
        });
      });
    }
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