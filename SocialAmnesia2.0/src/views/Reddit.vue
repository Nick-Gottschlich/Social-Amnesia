<template>
  <div>
    <div class="redditContainer">
      <LoginPanel site="Reddit" />
    </div>
    <div class="pageDivider" />
    <div class="redditContainer paddingTop">
      <UserItemsPanel itemtype="comments" />
      <UserItemsPanel itemtype="posts" />
    </div>
  </div>
</template>

<script>
import LoginPanel from "@/components/shared/LoginPanel.vue";
import UserItemsPanel from "@/components/reddit/UserItemsPanel.vue";

export default {
  name: "Twitter",
  components: {
    LoginPanel,
    UserItemsPanel
  }
};
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
