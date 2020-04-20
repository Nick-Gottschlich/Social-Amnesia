<template>
  <div>
    <div class="twitterContainer">
      <LoginPanel />
      <DeletionPanel />
    </div>
    <div class="twitterContainer paddingTop">
      <UserItemsPanel itemType="tweets" />
      <UserItemsPanel itemType="favorites" />
    </div>
  </div>
</template>

<script>
import LoginPanel from "@/components/twitter/LoginPanel.vue";
import UserItemsPanel from "@/components/twitter/UserItemsPanel.vue";
import DeletionPanel from '@/components/twitter/DeletionPanel.vue'

export default {
  name: "Twitter",
  components: {
    LoginPanel,
    UserItemsPanel,
    DeletionPanel
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