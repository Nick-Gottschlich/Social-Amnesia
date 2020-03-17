<template>
  <div>
    <button v-on:click="handleTwitterLogin()">Login to twitter</button>
    <span>{{ loginMessage }}</span>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
// import axios from "axios";
import Twitter from "twitter-lite";
import twitterApi from "../../secrets";

@Component
export default class TwitterLogin extends Vue {
  userTweets = [];

  loginMessage = "Not Logged in!";

  handleTwitterLogin = () => {
    const client = new Twitter({
      // subdomain: "cors-anywhere.herokuapp.com/https://api",
      consumer_key: twitterApi.consumer_key,
      consumer_secret: twitterApi.consumer_secret
    });

    client
      .getRequestToken("https://localhost")
      .then(res => {
        console.log({
          reqTkn: res.oauth_token,
          reqTknSecret: res.oauth_token_secret
        });

        window.open(
          `https://api.twitter.com/oauth/authenticate?oauth_token=${res.oauth_token}`,
          "_blank",
        );

        this.loginMessage = "Logged in as _______";

        
      })
      .catch(console.error);
  };

  // mounted() {
  //   // const T = new Twit({
  //   //   consumer_key: twitterApi.consumer_key,
  //   //   consumer_secret: twitterApi.consumer_secret,
  //   //   access_token: twitterApi.access_token,
  //   //   access_token_secret: twitterApi.access_token_secret
  //   // });
  //   // T.post(
  //   //   "oauth/request_token",
  //   //   {
  //   //     // ouath_callback: "https://localhost",
  //   //     // oauth_consumer_key: twitterApi.consumer_key,
  //   //   },
  //   //   (err, data, response) => {
  //   //     console.log("err", err);
  //   //     console.log("data", data);
  //   //     console.log("resoonse", response);
  //   //     this.loginMessage = "Logged in as _______";
  //   //   }
  //   // );
  //   // T.post(
  //   //   "statuses/update",
  //   //   {
  //   //     status: "test tweet from api"
  //   //   },
  //   //   (err, data, response) => {
  //   //     console.log("err", err);
  //   //     console.log("data", data);
  //   //     console.log("resoonse", response);
  //   //     this.loginMessage = "Logged in as _______";
  //   //   }
  //   // )
  //   // T.get(
  //   //   "statuses/user_timeline",
  //   //   { count: 100, screen_name: "NickGottschlich" },
  //   //   (err, data, response) => {
  //   //     this.userTweets = data;
  //   //   }
  //   // );
  // }
}
</script>
