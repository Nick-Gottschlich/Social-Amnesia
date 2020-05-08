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
        <span class="loginMessage" v-bind:class="{ loginError, loggedIn }">{{ loginMessage }}</span>
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
import constants from "@/store/constants";
import twitterApi from "@/secrets";

const TWEETS_ROUTE = "statuses/user_timeline";
const FAVORITES_ROUTE = "favorites/list";

@Component
export default class LoginPanel extends Vue {
  loginError = false;

  loginMessage = "Not logged in!";

  get loggedIn() {
    if (store.state[constants.TWITTER_LOGGED_IN]) {
      this.loginMessage = `Logged in to twitter as @${
        store.state[constants.TWITTER_SCREEN_NAME]
      }`;
    }

    return store.state[constants.TWITTER_LOGGED_IN];
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
      store.state[constants.TWITTER_USER_CLIENT]
        .get(apiRoute, data)
        .then(tweets => {
          if (
            tweets.length === 0 ||
            (tweets.length === 1 && tweets[0].id === oldest)
          ) {
            if (apiRoute === TWEETS_ROUTE) {
              store.dispatch(constants.UPDATE_USER_TWEETS, userTweets);
            }
            if (apiRoute === FAVORITES_ROUTE) {
              store.dispatch(constants.UPDATE_USER_FAVORITES, userFavorites);
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

          store.dispatch(constants.UPDATE_TWITTER_USER_KEYS, {
            consumer_key: twitterApi.consumer_key,
            consumer_secret: twitterApi.consumer_secret,
            access_token_key: verificationResponse.oauth_token,
            access_token_secret: verificationResponse.oauth_token_secret
          });
          store.dispatch(
            constants.UPDATE_USER_CLIENT,
            new Twitter(store.state[constants.TWITTER_USER_KEYS])
          );

          store.dispatch(
            constants.UPDATE_TWITTER_SCREEN_NAME,
            verificationResponse.screen_name
          );
          store.dispatch(constants.UPDATE_USER_TWEETS, []);
          store.dispatch(constants.UPDATE_USER_FAVORITES, []);

          gatherItems({
            verificationResponse,
            apiRoute: "statuses/user_timeline"
          });
          gatherItems({ verificationResponse, apiRoute: "favorites/list" });

          store.dispatch(constants.LOGIN_TO_TWITTER);
          this.loginMessage = `Logged in to twitter as @${
            store.state[constants.TWITTER_SCREEN_NAME]
          }`;
          twitterApiWindow.close();
        })
        .catch(error => {
          // eslint-disable-next-line no-console
          console.error(`Failed to login to twitter with error ${JSON.stringify(error)}`);
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
          `Failed to load twitter api window with error: ${JSON.stringify(error)}s`
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

  .loggedIn {
    color: #218838;
  }
}
</style>
