<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">About</router-link>{{ " |" }}
      <router-link to="/twitter">Twitter</router-link>{{ " |" }}
      <router-link to="/reddit">Reddit</router-link>
    </div>
    <router-view />
  </div>
</template>

<script>
import store from "@/store/index";
import constants from "@/store/constants";
import helpers from "@/util/helpers";
import schedule from "node-schedule";

// Twitter scheduler
if (
  store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED].tweets ||
  store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED].favorites
) {
  const hours = store.state.twitter[constants.TWITTER_SCHEDULE_TIME].split(
    ":"
  )[0];
  const minutes = store.state.twitter[constants.TWITTER_SCHEDULE_TIME].split(
    ":"
  )[1];

  schedule.scheduleJob(`${minutes} ${hours} * * *`, () => {
    if (
      store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED].tweets
    ) {
      helpers.deleteTwitterItems(
        store.state.twitter[constants.USER_TWEETS],
        "twitter tweets",
        store.state.twitter[constants.WHITELISTED_TWEETS],
        true
      );

      helpers.twitterGatherAndSetItems({
        apiRoute: "statuses/user_timeline",
        itemArray: []
      });
    }

    if (
      store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED].favorites
    ) {
      helpers.deleteTwitterItems(
        store.state.twitter[constants.USER_FAVORITES],
        "twitter favorites",
        store.state.twitter[constants.WHITELISTED_FAVORITES],
        true
      );

      helpers.twitterGatherAndSetItems({
        apiRoute: "favorites/list",
        itemArray: []
      });
    }
  });
}

export default {
  name: "app"
};
</script>

<style lang="scss">
#app {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Ubuntu, "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
