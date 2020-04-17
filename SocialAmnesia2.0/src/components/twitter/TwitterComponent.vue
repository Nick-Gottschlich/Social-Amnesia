<template>
  <div class="allContainer">
    <div class="controls">
      <div class="loginContainer">
        <h1>Log in to Twitter</h1>
        <b-button
          class="loginButton"
          variant="success"
          v-on:click="handleTwitterLogin()"
        >Click to login</b-button>
        <span class="loginMessage" v-bind:class="{ loginError, loginSuccess }">{{ loginMessage }}</span>
      </div>
      <div class="deletionContainer" v-if="loginSuccess">
        <h1>Clean Twitter</h1>
        <div class="deletionButtonContainer">
          <b-button
            class="deletionButton"
            variant="danger"
            v-on:click="handleDeleteTweets()"
          >Click to delete tweets</b-button>
          <b-button variant="danger" v-on:click="handleDeleteTweets()">Click to delete ❤️'s</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
import Twitter from "twitter-lite";
import electron from "electron";
import store from "@/store/index";

import twitterApi from "../../secrets";

const TWEETS_ROUTE = "statuses/user_timeline";
const FAVORITES_ROUTE = "favorites/list";

@Component
export default class TwitterComponent extends Vue {
  loginSuccess = false;

  loginError = false;

  loginMessage = "Not logged in!";

  userClient;

  handleDeleteTweets() {
    store.state.userTweets.forEach(tweet => {
      this.userClient.post("statuses/destroy", {
        id: tweet.id_str
      });
    });
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
    let userFavorites = [];
    let oldest;

    const gatherItems = ({ verificationResponse, maxId, apiRoute }) => {
      const data = {
        tweet_mode: "extended",
        user_id: verificationResponse.user_id,
        // can only do 200 per request, so we need to continually make requests until we run out of tweets
        count: 200
      };
      if (maxId) {
        data.max_id = String(maxId);
      }
      this.userClient.get(apiRoute, data).then(tweets => {
        if (tweets.length === 1 && tweets[0].id === oldest) {
          if (apiRoute === TWEETS_ROUTE) {
            store.commit("updateUserTweets", userTweets);
          }
          if (apiRoute === FAVORITES_ROUTE) {
            store.commit("updateUserFavorites", userFavorites);
          }
          return;
        }

        if (apiRoute === TWEETS_ROUTE) {
          userTweets = userTweets.concat(tweets);
          oldest = userTweets.slice(-1)[0].id;
        }

        if (apiRoute === FAVORITES_ROUTE) {
          userFavorites = userFavorites.concat(tweets);
          oldest = userFavorites.slice(-1)[0].id;
        }

        gatherItems({ verificationResponse, maxId: oldest, apiRoute });
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
            this.loginError = true;
            throw Error(verificationResponse);
          }

          this.userClient = new Twitter({
            consumer_key: twitterApi.consumer_key,
            consumer_secret: twitterApi.consumer_secret,
            access_token_key: verificationResponse.oauth_token,
            access_token_secret: verificationResponse.oauth_token_secret
          });

          gatherItems({
            verificationResponse,
            apiRoute: "statuses/user_timeline"
          });
          gatherItems({ verificationResponse, apiRoute: "favorites/list" });

          this.loginSuccess = true;
          store.commit("logInToTwitter");
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

<style lang="scss">
.allContainer {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Ubuntu, "Helvetica Neue", sans-serif;
}

.controls {
  display: flex;
  justify-content: space-around;
}

.loginContainer {
  display: flex;
  flex-direction: column;
  align-items: center;

  border: 4mm ridge #218838;
  padding: 20px;
  margin-top: 10px;

  .loginButton {
    width: 150px;
  }

  .loginMessage {
    padding-top: 10px;
  }

  .loginError {
    color: #dc3545;
  }

  .loginSuccess {
    color: #218838;
  }
}

.deletionContainer {
  border: 4mm ridge #dc3545;
  padding: 20px;
  margin-top: 10px;

  .deletionButtonContainer {
    display: flex;
    flex-direction: column;

    .deletionButton {
      margin-bottom: 5px;
    }
  }
}
</style>
