<template>
  <div>
    <div class="twitterContainer">
      <LoginPanel />
      <ControlPanel />
      <DeletionPanel />
    </div>
    <div class="twitterContainer paddingTop">
      <UserItemsPanel itemtype="tweets" />
      <UserItemsPanel itemtype="favorites" />
    </div>
    <ProgressBar />
  </div>
</template>

<script>
import LoginPanel from "@/components/twitter/LoginPanel.vue";
import UserItemsPanel from "@/components/twitter/UserItemsPanel.vue";
import DeletionPanel from "@/components/twitter/DeletionPanel.vue";
import ProgressBar from "@/components/ProgressBar.vue";
import ControlPanel from "@/components/ControlPanel.vue";

export default {
  name: "Twitter",
  components: {
    LoginPanel,
    UserItemsPanel,
    DeletionPanel,
    ProgressBar,
    ControlPanel
  }
};
</script>

<style lang="scss">
.twitterContainer {
  display: flex;
  justify-content: space-around;
}

.paddingTop {
  padding-top: 20px;
}
</style>
