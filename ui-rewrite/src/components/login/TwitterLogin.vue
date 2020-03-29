<template>
  <div>
    <button v-on:click="handleTwitterLogin()">Login to twitter</button>
    <span>{{ loginMessage }}</span>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
import Twitter from "twitter-lite";
import electron from "electron";

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
        const mainWindow = electron.remote.getCurrentWindow();

        twitterApiWindow = new BrowserWindow({
          parent: mainWindow,
          modal: true
        });
        twitterApiWindow.loadURL(
          `https://api.twitter.com/oauth/authenticate?oauth_token=${res.oauth_token}`
        );
        twitterApiWindow.webContents.on("did-navigate", (event, url) => {
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
                userClient = new Twitter({
                  consumer_key: twitterApi.consumer_key,
                  consumer_secret: twitterApi.consumer_secret,
                  access_token_key: response.oauth_token,
                  access_token_secret: response.oauth_token_secret
                });

                userClient
                  .get("statuses/user_timeline", {
                    user_id: response.user_id
                  })
                  .then(userTweets => {
                    console.log("userTweets", userTweets);
                    twitterApiWindow.close();
                  });
              })
              .catch(error => {
                console.error(error);
                // TODO: display some kind of "failed to login to twitter" message 
                twitterApiWindow.close();
              });
          }
        });

        this.loginMessage = "Logged in as _______";
      })
      .catch(console.error);
  };
}
</script>
