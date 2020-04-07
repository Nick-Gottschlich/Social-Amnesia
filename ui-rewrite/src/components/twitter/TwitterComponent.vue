<template>
  <div>
    <button v-on:click="handleTwitterLogin()">Login to twitter</button>
    <span>{{ loginMessage }}</span>
    <button v-if="loggedIn" v-on:click="handleDeleteTweets()">Delete your tweets</button>
    <ul>
      <li v-for="tweet in userTweetsToDisplay" :key="tweet.id">{{tweet.text}}</li>
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
  userTweetsToDisplay = [];

  loggedIn = false;

  loginMessage = "Not logged in!";

  userClient;

  handleDeleteTweets() {
    this.userTweetsToDisplay.forEach((tweet) => {
      this.userClient.post("statuses/destroy", {
        id: tweet.id_str
      });
    })
  }

  handleTwitterLogin() {
    const client = new Twitter({
      consumer_key: twitterApi.consumer_key,
      consumer_secret: twitterApi.consumer_secret
    });
    let oauth_verifier;
    const { BrowserWindow } = electron.remote;
    const mainWindow = electron.remote.getCurrentWindow();
    const twitterApiWindow = new BrowserWindow({
      parent: mainWindow
      // modal: true
    });
    let userTweets = [];
    let oldest;

    const gatherTweets = (verificationResponse, maxId) => {
      const data = {
        user_id: verificationResponse.user_id,
        // can only do 200 per request, so we need to continually make requests until we run out of tweets
        count: 200
      };
      if (maxId) {
        data.max_id = String(maxId);
      }
      this.userClient.get("statuses/user_timeline", data).then(tweets => {
        if (tweets.length === 1 && tweets[0].id === oldest) {
          this.userTweetsToDisplay = userTweets;
          return;
        }

        userTweets = userTweets.concat(tweets);
        oldest = userTweets.slice(-1)[0].id;
        gatherTweets(verificationResponse, oldest);
      });
    };

    const makeFollowUpRequest = initialResponse => {
      client
        .getAccessToken({
          key: initialResponse.oauth_token,
          secret: initialResponse.oauth_token_secret,
          verifier: oauth_verifier
        })
        .then(verificationResponse => {
          if (
            !verificationResponse.oauth_token ||
            !verificationResponse.oauth_token_secret
          ) {
            // login has failed, abort
            this.loginMessage = "Failed to login to twitter!";
            throw Error(verificationResponse);
          }

          this.userClient = new Twitter({
            consumer_key: twitterApi.consumer_key,
            consumer_secret: twitterApi.consumer_secret,
            access_token_key: verificationResponse.oauth_token,
            access_token_secret: verificationResponse.oauth_token_secret
          });

          gatherTweets(verificationResponse);

          this.loggedIn = true;
          this.loginMessage = `Logged in to twitter as ${verificationResponse.screen_name}`;
          twitterApiWindow.close();
        })
        .catch(error => {
          // eslint-disable-next-line no-console
          console.error(`Failed to login to twitter with error ${error}`);
          twitterApiWindow.close();
        });
    };

    client
      .getRequestToken("https://google.com")
      .then(initialResponse => {
        twitterApiWindow.loadURL(
          `https://api.twitter.com/oauth/authenticate?oauth_token=${initialResponse.oauth_token}`
        );
        twitterApiWindow.webContents.on("did-navigate", (event, url) => {
          if (url.indexOf("google") >= 0) {
            const searchParams = new URLSearchParams(url.slice(23));
            oauth_verifier = searchParams.get("oauth_verifier");

            makeFollowUpRequest(initialResponse);
          }
        });
      })
      .catch(error => {
        // eslint-disable-next-line no-console
        console.error(
          `Failed to load twitter api window with error: ${error}s`
        );
      });
  }
}
</script>
