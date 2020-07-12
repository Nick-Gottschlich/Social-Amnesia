<template>
  <div>
    <div class="twitterContainer">
      <LoginPanel site="Twitter" />
      <DeletionPanel site="Twitter" />
    </div>
    <div class="controlPanel">
      <TimeRange site="Twitter" />
      <ScorePanel site="Twitter" />
    </div>
    <div class="pageDivider" />
    <div class="refreshItemsButtonContainer">
      <RefreshItemsButton site="Twitter" />
    </div>
    <div class="twitterContainer paddingTop">
      <UserItemsPanel itemtype="tweets" />
      <UserItemsPanel itemtype="favorites" />
    </div>
    <ProgressBar />
  </div>
</template>

<script>
import LoginPanel from "@/components/shared/LoginPanel.vue";
import UserItemsPanel from "@/components/twitter/UserItemsPanel.vue";
import DeletionPanel from "@/components/shared/DeletionPanel.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import TimeRange from "@/components/shared/ControlPanel/TimeRange.vue";
import ScorePanel from "@/components/shared/ControlPanel/ScorePanel.vue";
import RefreshItemsButton from "@/components/shared/RefreshItemsButton.vue";
import helpers from "@/util/helpers";
import store from "@/store/index";
import constants from "@/store/constants";

export default {
  name: "Twitter",
  components: {
    LoginPanel,
    UserItemsPanel,
    DeletionPanel,
    ProgressBar,
    TimeRange,
    ScorePanel,
    RefreshItemsButton
  }
};

if (store.state.twitter[constants.TWITTER_LOGGED_IN]) {
  // when the app is loaded, automatically refresh items
  helpers.twitterGatherAndSetItems({
    apiRoute: "statuses/user_timeline",
    itemArray: []
  });
  helpers.twitterGatherAndSetItems({
    apiRoute: "favorites/list",
    itemArray: []
  });
}
</script>

<style lang="scss">
.twitterContainer {
  display: flex;
  justify-content: space-around;
}

.paddingTop {
  padding-top: 20px;
}

.controlPanel {
  padding: 20px;
  display: flex;
  justify-content: space-between;
}

.pageDivider {
  border-bottom: 1px solid grey;
  margin-bottom: 20px;
}
</style>
