<template>
  <div>
  <h1>
    SOCIAL AMNESIA 2.0
  </h1>
  <div id="test">
    <ul>
      <li v-for="tweet in userTweets" :key="tweet.id">
        {{ tweet.text }}
      </li>
    </ul>
    {{ userTweets }}
  </div>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
// import axios from "axios";
// import Twit from "twit";
import twitterApi from "../secrets";

@Component
export default class Test extends Vue {
  userTweets = [];

  // mounted() {
  //   const T = new Twit({
  //     consumer_key: twitterApi.consumer_key,
  //     consumer_secret: twitterApi.consumer_secret,
  //     access_token: twitterApi.access_token,
  //     access_token_secret: twitterApi.access_token_secret
  //   });

  //   T.get(
  //     "statuses/user_timeline",
  //     { count: 100, screen_name: "NickGottschlich" },
  //     (err, data, response) => {
  //       this.userTweets = data;
  //     }
  //   );
  // }
}
</script>
