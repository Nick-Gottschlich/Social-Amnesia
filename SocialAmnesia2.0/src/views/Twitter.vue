<template>
  <div>
    <TwitterComponent />
    <div class="userItemsContainer">
      <UserItemsPanel itemType="tweets" />
      <UserItemsPanel itemType="favorites" />
    </div>
  </div>
</template>

<script>
import TwitterComponent from "@/components/twitter/TwitterComponent.vue";
import UserItemsPanel from "@/components/twitter/UserItemsPanel.vue";

export default {
  name: "Twitter",
  components: {
    TwitterComponent,
    UserItemsPanel
  }
};
</script>

<style lang="scss">
.userItemsContainer {
  display: flex;
}
</style>