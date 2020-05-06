<template>
  <div>
    <div class="twitterContainer">
      <LoginPanel />
      <DeletionPanel />
    </div>
    <div class="twitterContainer paddingTop">
      <UserItemsPanel itemtype="tweets" />
      <UserItemsPanel itemtype="favorites" />
    </div>
    <b-button v-b-modal.modal-1>Launch demo modal</b-button>

    <b-modal
      id="modal-1"
      title="Deleting your items..."
      centered
      no-close-on-backdrop
      no-close-on-esc
      hide-footer
      hide-header-close
    >
      <b-progress :value="20" :max="100" show-progress animated>
        <b-progress-bar :value="20">40/200</b-progress-bar>
      </b-progress>
    </b-modal>
  </div>
</template>

<script>
import LoginPanel from "@/components/twitter/LoginPanel.vue";
import UserItemsPanel from "@/components/twitter/UserItemsPanel.vue";
import DeletionPanel from "@/components/twitter/DeletionPanel.vue";

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