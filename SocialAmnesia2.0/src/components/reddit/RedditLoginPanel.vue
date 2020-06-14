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
import { Component, Vue } from "vue-property-decorator";
import Snoowrap from "snoowrap";
import electron from "electron";
import redditAPI from "@/redditSecrets";

@Component
export default class RedditLoginPanel extends Vue {
  handleRedditLogin() {
    console.log("clicked");
    let redditClient;

    const { BrowserWindow } = electron.remote;
    const mainWindow = electron.remote.getCurrentWindow();
    const redditAPIWindow = new BrowserWindow({
      parent: mainWindow
    });

    redditAPIWindow.loadURL(
      `https://www.reddit.com/api/v1/authorize?client_id=${redditAPI.clientId}&response_type=code&state=randomString&redirect_uri=https://google.com&duration=permanent&scope=identity,history,read,edit`
    );

    redditAPIWindow.webContents.on("did-navigate", (event, url) => {
      if (url.indexOf("google") >= 0) {
        const searchParams = new URLSearchParams(url.slice(23));
        const oauthCode = searchParams.get("code");
        console.log("oauth code", oauthCode);

        redditClient = new Snoowrap({
          userAgent: redditAPI.userAgent,
          clientId: redditAPI.clientId,
          clientSecret: redditAPI.clientSecret,
          refreshToken: oauthCode
        });

        redditClient
          .getHot()
          .map(post => post.title)
          .then(console.log);
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
