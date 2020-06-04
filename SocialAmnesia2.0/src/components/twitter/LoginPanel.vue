<template>
  <div class="allContainer">
    <div class="controls">
      <div class="loginContainer">
        <h1>Log in to Twitter</h1>
        <b-button
          class="loginButton"
          variant="success"
          v-on:click="handleTwitterLogin()"
          v-if="!loggedIn"
        >
          Click to login
        </b-button>
        <div id="login-panel-login-button">
          <b-button
            class="loginButton"
            variant="success"
            v-on:click="handleTwitterLogout()"
            v-if="loggedIn"
          >
            Click to logout
          </b-button>
        </div>
        <b-tooltip
          target="login-panel-login-button"
          triggers="hover"
          placement="bottom"
        >
          This will clear your saved settings!
        </b-tooltip>
        <span class="loginMessage" v-bind:class="{ loginError, loggedIn }">
          {{ loginMessage }}
        </span>
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
import helpers from "@/util/helpers";

@Component
export default class LoginPanel extends Vue {
  loginError = false;

  loginMessage = "Not logged in!";

  get loggedIn() {
    if (store.state.twitter[constants.TWITTER_LOGGED_IN]) {
      this.loginMessage = `Logged in to twitter as @${
        store.state.twitter[constants.TWITTER_SCREEN_NAME]
      }`;
    }

    return store.state.twitter[constants.TWITTER_LOGGED_IN];
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
            constants.UPDATE_TWITTER_USER_CLIENT,
            new Twitter(store.state.twitter[constants.TWITTER_USER_KEYS])
          );

          store.dispatch(
            constants.UPDATE_TWITTER_SCREEN_NAME,
            verificationResponse.screen_name
          );
          store.dispatch(
            constants.UPDATE_TWITTER_USER_ID,
            verificationResponse.user_id
          );

          // Clear out existing items and white list
          // This can be removed once I add a log out button
          //  that can clear store/persistence
          store.dispatch(constants.UPDATE_USER_TWEETS, []);
          store.dispatch(constants.UPDATE_USER_FAVORITES, []);
          store.dispatch(constants.UPDATE_WHITELISTED_TWEETS, -1);
          store.dispatch(constants.UPDATE_WHITELISTED_FAVORITES, -1);

          helpers.gatherAndSetItems({
            apiRoute: "statuses/user_timeline",
            itemArray: []
          });
          helpers.gatherAndSetItems({
            apiRoute: "favorites/list",
            itemArray: []
          });

          store.dispatch(constants.LOGIN_TO_TWITTER);
          this.loginMessage = `Logged in to twitter as @${
            store.state.twitter[constants.TWITTER_SCREEN_NAME]
          }`;
          twitterApiWindow.close();
        })
        .catch(error => {
          // eslint-disable-next-line no-console
          console.error("Failed to login to twitter with error:", error);
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
          `Failed to load twitter api window with error: ${JSON.stringify(
            error
          )}s`
        );
      });
  }

  handleTwitterLogout() {
    const { BrowserWindow } = electron.remote;
    const mainWindow = electron.remote.getCurrentWindow();
    // this removes the cookie that will auto login to twitter
    mainWindow.webContents.session.cookies.remove(
      "https://twitter.com",
      "auth_token"
    );

    this.loginMessage = "Not Logged In!";
    store.dispatch(constants.LOGOUT_OF_TWITTER);
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
