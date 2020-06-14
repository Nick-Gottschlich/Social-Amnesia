<template>
  <div>
    <div class="redditLoginAndDeleteContainer">
      <RedditLoginPanel />
    </div>
  </div>
</template>

<script>
import RedditLoginPanel from "@/components/reddit/RedditLoginPanel.vue";

export default {
  name: "Twitter",
  components: {
    RedditLoginPanel
  }
};
</script>
