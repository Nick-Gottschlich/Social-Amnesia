<template>
  <div>
    <TwitterComponent />
    <UserTweetsPanel />
  </div>
</template>

<script>
import TwitterComponent from "@/components/twitter/TwitterComponent.vue";
import UserTweetsPanel from "@/components/twitter/UserTweetsPanel.vue";

export default {
  name: "Twitter",
  components: {
    TwitterComponent,
    UserTweetsPanel,
  }
};
</script>