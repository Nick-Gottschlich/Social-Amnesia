<template>
  <div>
    <button v-on:click="handleTwitterLogin()">Login to twitter</button>
    <span>{{ loginMessage }}</span>
    <button v-if="loggedIn" v-on:click="handleDeleteTweets()">Delete your tweets</button>
    <ul>
      <li v-for="tweet in userTweets" :key="tweet.id">{{tweet.text}}</li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
import Twitter from "twitter-lite";
import electron from "electron";

import twitterApi from "../../secrets";

@Component
export default class TwitterComponent extends Vue {
  userTweets = [];

  loggedIn = false;

  loginMessage = "Not logged in!";

  handleDeleteTweets() {
    console.log("delete tweets clicked", this.loggedIn);
  }

  handleTwitterLogin() {
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
      .then(initialResponse => {
        const mainWindow = electron.remote.getCurrentWindow();

        twitterApiWindow = new BrowserWindow({
          parent: mainWindow,
          modal: true
        });
        twitterApiWindow.loadURL(
          `https://api.twitter.com/oauth/authenticate?oauth_token=${initialResponse.oauth_token}`
        );
        twitterApiWindow.webContents.on("did-navigate", (event, url) => {
          if (url.indexOf("google") >= 0) {
            const searchParams = new URLSearchParams(url.slice(23));
            oauth_verifier = searchParams.get("oauth_verifier");

            client
              .getAccessToken({
                key: initialResponse.oauth_token,
                secret: initialResponse.oauth_token_secret,
                verifier: oauth_verifier
              })
              .then((verificationResponse, error) => {
                if (
                  !verificationResponse.oauth_token ||
                  !verificationResponse.oauth_token_secret
                ) {
                  // login has failed, abort
                  this.loginMessage = "Failed to login to twitter!";
                  throw Error(verificationResponse);
                }

                userClient = new Twitter({
                  consumer_key: twitterApi.consumer_key,
                  consumer_secret: twitterApi.consumer_secret,
                  access_token_key: verificationResponse.oauth_token,
                  access_token_secret: verificationResponse.oauth_token_secret
                });

                userClient
                  .get("statuses/user_timeline", {
                    user_id: verificationResponse.user_id,
                    // can only do 200 per request, so this is where we need to continually make requests until we run out of tweets
                    count: 200
                  })
                  .then(userTweets => {
                    this.userTweets = userTweets;
                    console.log('user tweets', userTweets)
                    this.loggedIn = true;
                    this.loginMessage = `Logged in to twitter as ${verificationResponse.screen_name}`;
                    twitterApiWindow.close();
                  });
              })
              .catch(error => {
                console.error(`Failed to login to twitter with error ${error}`);
                twitterApiWindow.close();
              });
          }
        });
      })
      .catch(error => {
        console.error(
          `Failed to load twitter api window with error: ${error}s`
        );
      });
  }
}
</script>
