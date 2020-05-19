<template>
  <b-button
    class="refreshButton"
    variant="primary"
    v-on:click="handleRefreshClick()"
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

@Component
export default class RefreshItemsButton extends Vue {
  loading = false;

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
