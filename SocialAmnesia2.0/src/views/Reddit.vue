<template>
  <div>
    <div class="redditContainer">
      <LoginPanel site="Reddit" />
      <DeletionPanel site="Reddit" />
    </div>
    <div class="pageDivider" />
    <div class="refreshItemsButtonContainer">
      <RefreshItemsButton site="Reddit" />
    </div>
    <div class="redditContainer paddingTop">
      <UserItemsPanel itemtype="comments" />
      <UserItemsPanel itemtype="posts" />
    </div>
    <ProgressBar />
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import LoginPanel from "@/components/shared/LoginPanel.vue";
import UserItemsPanel from "@/components/reddit/UserItemsPanel.vue";
import RefreshItemsButton from "@/components/shared/RefreshItemsButton.vue";
import DeletionPanel from "@/components/shared/DeletionPanel.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import helpers from "@/util/helpers";
import store from "@/store/index";
import constants from "@/store/constants";

export default {
  name: "Twitter",
  components: {
    LoginPanel,
    UserItemsPanel,
    RefreshItemsButton,
    DeletionPanel,
    ProgressBar
  }
};

if (store.state.reddit[constants.REDDIT_LOGGED_IN]) {
  helpers.stopRedditAccessTokenRefresh();
  helpers.refreshRedditAccessToken();
}
</script>

<style lang="scss">
.redditContainer {
  display: flex;
  justify-content: space-around;
}

.pageDivider {
  padding-top: 20px;
  border-bottom: 1px solid grey;
}

.paddingTop {
  padding-top: 20px;
}
</style>
