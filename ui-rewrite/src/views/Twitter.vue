<template>
  <div>
    <h1>Login here!</h1>
    <TwitterComponent />
  </div>
</template>

<script>
import TwitterComponent from "@/components/twitter/TwitterComponent.vue";

export default {
  name: "Twitter",
  components: {
    TwitterComponent,
  },
};
</script>