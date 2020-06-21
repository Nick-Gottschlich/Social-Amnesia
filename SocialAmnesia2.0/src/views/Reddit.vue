<template>
  <div>
    <div class="redditLoginAndDeleteContainer">
      <LoginPanel site="Reddit" />
    </div>
  </div>
</template>

<script>
import LoginPanel from "@/components/shared/LoginPanel.vue";

export default {
  name: "Twitter",
  components: {
    LoginPanel
  }
};
</script>

<style lang="scss">
.twitterLoginAndDeleteContainer {
  display: flex;
  justify-content: space-around;
}
</style>
