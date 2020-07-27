<template>
  <b-button
    class="refreshButton"
    variant="primary"
    v-on:click="handleRefreshClick()"
    v-if="loggedIn"
  >
    <span v-if="!this.loading">
      Refresh {{ site === "Twitter" ? "tweets/favorites" : "comments/posts" }}
    </span>
    <b-spinner v-if="this.loading" />
  </b-button>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import helpers from "@/util/helpers";
import store from "@/store/index";
import constants from "@/store/constants";

const RefreshItemsButtonProps = Vue.extend({
  props: {
    site: String
  }
});

@Component
export default class RefreshItemsButton extends RefreshItemsButtonProps {
  loading = false;

  get loggedIn() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_LOGGED_IN]
      : store.state.reddit[constants.REDDIT_LOGGED_IN];
  }

  handleRefreshClick() {
    this.loading = true;

    if (this.site === "Twitter") {
      helpers.twitterGatherAndSetItems({
        apiRoute: "statuses/user_timeline",
        itemArray: []
      });
      helpers.twitterGatherAndSetItems({
        apiRoute: "favorites/list",
        itemArray: []
      });
    } else if (this.site === "Reddit") {
      helpers.redditGatherAndSetItems();
    }
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }
}
</script>
