<template>
  <div class="loginContainer">
    <h1>Log in to Reddit</h1>
    <b-button
      class="redditLogButton"
      variant="success"
      v-on:click="handleRedditLogin()"
      v-if="!loggedIn"
    >
      Click to login
    </b-button>
    <div id="login-panel-logout-button">
      <b-button
        class="redditLogButton"
        variant="success"
        v-on:click="handleTwitterLogout()"
        v-if="loggedIn"
      >
        Click to logout
      </b-button>
    </div>
    <b-tooltip
      target="login-panel-logout-button"
      triggers="hover"
      placement="bottom"
    >
      This will clear your saved settings!
    </b-tooltip>
    <span class="loginMessage" v-bind:class="{ loginError, loggedIn }">
      {{ loginMessage }}
    </span>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
import electron from "electron";
import axios from "axios";
import redditAPI from "@/redditSecrets";
import constants from "@/store/constants";
import store from "@/store/index";

@Component
export default class RedditLoginPanel extends Vue {
  loginError = false;

  loginMessage = "Not logged in!";

  get loggedIn() {
    if (store.state.reddit[constants.REDDIT_LOGGED_IN]) {
      this.loginMessage = `Logged in to reddit as @${
        store.state.reddit[constants.REDDIT_USER_NAME]
      }`;
    }

    return store.state.reddit[constants.REDDIT_LOGGED_IN];
  }

  handleRedditLogin() {
    const { BrowserWindow } = electron.remote;
    const mainWindow = electron.remote.getCurrentWindow();
    const redditAPIWindow = new BrowserWindow({
      parent: mainWindow
    });

    redditAPIWindow.loadURL(
      `https://www.reddit.com/api/v1/authorize?client_id=${redditAPI.clientId}&response_type=code&state=randomString&redirect_uri=https://google.com&duration=permanent&scope=identity,history,read,edit`
    );

    redditAPIWindow.webContents.on("did-navigate", (event, url) => {
      if (url.indexOf("google") >= 0 && url.indexOf("reddit") === -1) {
        const searchParams = new URLSearchParams(url.slice(23));
        const oauthCode = searchParams.get("code");
        redditAPIWindow.close();

        axios
          .post(
            "https://www.reddit.com/api/v1/access_token",
            {},
            {
              params: {
                grant_type: "authorization_code",
                code: oauthCode,
                redirect_uri: "https://google.com"
              },
              auth: {
                username: redditAPI.clientId,
                password: ""
              }
            }
          )
          .then(response => {
            console.log(response.data.access_token);

            const accessToken = response.data.access_token;

            store.dispatch(constants.LOGIN_TO_REDDIT);
            store.dispatch(
              constants.UPDATE_REDDIT_ACCESS_TOKEN,
              response.data.access_token
            );

            // TODO(NG): move this to a helper function
            axios
              .get("https://oauth.reddit.com/api/v1/me", {
                headers: {
                  Authorization: `bearer ${accessToken}`
                }
              })
              .then(loginResponse => {
                console.log("api me response", loginResponse);

                store.dispatch(
                  constants.UPDATE_REDDIT_USER_NAME,
                  loginResponse.data.name
                );
              });
          })
          .catch(error => {
            console.error("Failed to login to reddit with error:", error);
            redditAPIWindow.close();
          });
      }
    });
  }

  handleTwitterLogout() {
    // TODO(NG): remove cookies that auto login to reddit

    this.loginMessage = "Not Logged In!";
    store.dispatch(constants.LOGOUT_OF_REDDIT);
  }
}
</script>

<style lang="scss">
.loginContainer {
  display: flex;
  flex-direction: column;
  align-items: center;

  border: 4mm ridge #218838;
  padding: 20px;
  margin-top: 10px;
}
</style>
