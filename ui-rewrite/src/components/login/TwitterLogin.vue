<template>
  <div>
    <button v-on:click="handleTwitterLogin()">Login to twitter</button>
    <span>{{ loginMessage }}</span>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
/* eslint-disable no-debugger */
import { Component, Vue } from "vue-property-decorator";
import Twitter from "twitter-lite";
import electron from "electron";
// import { BrowserWindow } from "electron";

import twitterApi from "../../secrets";

@Component
export default class TwitterLogin extends Vue {
  userTweets = [];

  loginMessage = "Not Logged in!";

  handleTwitterLogin = () => {
    const client = new Twitter({
      consumer_key: twitterApi.consumer_key,
      consumer_secret: twitterApi.consumer_secret
    });

    const { BrowserWindow } = electron.remote;
    let twitterApiWindow;
    let oauth_verifier;
    let userClient;

    client
      .getRequestToken("https://google.com")
      .then(res => {
        console.log({
          reqTkn: res.oauth_token,
          reqTknSecret: res.oauth_token_secret
        });

        twitterApiWindow = new BrowserWindow({});
        // twitterApiWindow = new BrowserWindow({});
        twitterApiWindow.loadURL(
          `https://api.twitter.com/oauth/authenticate?oauth_token=${res.oauth_token}`
        );
        console.log(twitterApiWindow.webContents);
        twitterApiWindow.webContents.on("did-navigate", (event, url) => {
          console.log("navigated to", url);
          if (url.indexOf("google") >= 0) {
            const searchParams = new URLSearchParams(url.slice(23));
            oauth_verifier = searchParams.get("oauth_verifier");

            client
              .getAccessToken({
                key: res.oauth_token,
                secret: res.oauth_token_secret,
                verifier: oauth_verifier
              })
              .then(response => {
                console.log({
                  accTkn: response.oauth_token,
                  accTknSecret: response.oauth_token_secret,
                  userId: response.user_id,
                  screenName: response.screen_name
                });

                userClient = new Twitter({
                  consumer_key: twitterApi.consumer_key,
                  consumer_secret: twitterApi.consumer_secret,
                  access_token_key: response.oauth_token,
                  access_token_secret: response.oauth_token_secret
                });

                const userTweets = userClient.get('statuses/user_timeline', {
                  user_id: response.user_id
                })

                console.log('userTweets', userTweets)
              })
              .catch(console.error);
          }
        });

        // debugger;

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
