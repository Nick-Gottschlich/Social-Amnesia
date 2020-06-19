<template>
  <div class="loginContainer">
    <h1>Log in to Reddit</h1>
    <b-button
      class="logButton"
      variant="success"
      v-on:click="handleRedditLogin()"
    >
      Click to login
    </b-button>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
import electron from "electron";
import axios from "axios";
import redditAPI from "@/redditSecrets";

@Component
export default class RedditLoginPanel extends Vue {
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
        console.log("URL", url);

        const searchParams = new URLSearchParams(url.slice(23));
        const oauthCode = searchParams.get("code");
        console.log("oauth code", oauthCode);

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

            // testing successful login...
            axios
              .get("https://oauth.reddit.com/api/v1/me", {
                headers: {
                  Authorization: `bearer ${accessToken}`
                }
              })
              .then(loginResponse => {
                console.log("api me response", loginResponse);
              });
          });
      }
    });
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
