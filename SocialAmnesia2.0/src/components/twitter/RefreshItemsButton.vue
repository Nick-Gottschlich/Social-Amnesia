<template>
  <b-button
    class="refreshButton"
    variant="primary"
    v-on:click="handleRefreshClick()"
    v-if="loggedIn"
  >
    <span v-if="!this.loading">
      Refresh tweets/favorites
    </span>
    <b-spinner v-if="this.loading" />
  </b-button>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import helpers from "@/util/helpers";
import store from "@/store/index";
import constants from "@/store/constants";

@Component
export default class RefreshItemsButton extends Vue {
  loading = false;

  get loggedIn() {
    return store.state[constants.TWITTER_LOGGED_IN];
  }

  handleRefreshClick() {
    this.loading = true;
    helpers.gatherAndSetItems({
      apiRoute: "statuses/user_timeline",
      itemArray: []
    });
    helpers.gatherAndSetItems({
      apiRoute: "favorites/list",
      itemArray: []
    });
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }
}
</script>
