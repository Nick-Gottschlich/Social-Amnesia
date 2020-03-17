<template>
  <div class="login">
    <h1>Login here!</h1>
    <TwitterLogin />
  </div>
</template>

<script>
import TwitterLogin from "@/components/login/TwitterLogin.vue";

export default {
  name: "Login",
  components: {
    TwitterLogin,
  },
};
</script>