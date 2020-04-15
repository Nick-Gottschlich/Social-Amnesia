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
    <!-- <div class="tweetsAndFavoritesContainer" v-if="loginSuccess">
      <div class="tweetsContainer">
        <h1>Your tweets</h1>
        <ul class="tweetList">
          <li class="tweet" v-for="tweet in userTweetsToDisplay" :key="tweet.id">
            <div class="tweetHeader">
              <img :src="tweet.user.profile_image_url_https" />
              <div class="tweetUsernames">
                <span class="tweetName">{{tweet.user.name}}</span>
                <span class="tweetUsername">@{{tweet.user.screen_name}}</span>
              </div>
            </div>
            <div class="tweetBody">
              <span class="tweetText">{{tweet.full_text}}</span>
              <div
                class="tweetMedia"
                v-if="tweet.extended_entities && tweet.extended_entities.media"
              >
                <li v-for="media in tweet.extended_entities.media" :key="media.media_url_https">
                  <img class="tweetImage" :src="media.media_url_https" />
                </li>
              </div>
              <span class="tweetCreatedAt">{{new Date(tweet.created_at).toLocaleString()}}</span>
            </div>
            <div class="tweetFooter">
              <div class="favorites">❤️{{tweet.favorite_count}}</div>
              <div class="retweets">🔁{{tweet.retweet_count}}</div>
            </div>
          </li>
        </ul>
      </div>
      <div class="favoritesContainer">Favorites</div>
    </div>-->
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
import Twitter from "twitter-lite";
import electron from "electron";
import store from '@/store/index';

import twitterApi from "../../secrets";

@Component
export default class TwitterComponent extends Vue {
  userTweetsToDisplay = [];

  loginSuccess = false;

  loginError = false;

  loginMessage = "Not logged in!";

  userClient;

  handleDeleteTweets() {
    this.userTweetsToDisplay.forEach(tweet => {
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
    let oldest;

    const gatherTweets = (verificationResponse, maxId) => {
      const data = {
        tweet_mode: "extended",
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
          console.log(this.userTweetsToDisplay);
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
            this.loginError = true;
            throw Error(verificationResponse);
          }

          this.userClient = new Twitter({
            consumer_key: twitterApi.consumer_key,
            consumer_secret: twitterApi.consumer_secret,
            access_token_key: verificationResponse.oauth_token,
            access_token_secret: verificationResponse.oauth_token_secret
          });

          gatherTweets(verificationResponse);

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

// .tweetsAndFavoritesContainer {
//   display: flex;
//   justify-content: space-between;

//   padding-top: 20px;
//   padding-left: 20px;
//   padding-right: 20px;

//   .tweetsContainer {
//     width: 48%;
//     border: 4mm ridge #1da1f2;

//     .tweetList {
//       padding-left: 0;
//     }

//     .tweet {
//       padding: 15px;
//       margin: 10px;
//       border: 1px solid #e1e8ed;
//       border-radius: 5px;
//       list-style: none;

//       &:hover {
//         background-color: #dddddd;
//       }

//       .tweetHeader {
//         display: flex;
//         justify-content: flex-start;

//         .tweetUsernames {
//           display: flex;
//           flex-direction: column;
//           align-items: flex-start;
//           padding-left: 5px;

//           .tweetName {
//             line-height: 1.3125;
//             font-weight: bold;
//           }
//           .tweetUsername {
//             color: #697882;
//           }
//         }
//       }

//       .tweetBody {
//         display: flex;
//         flex-direction: column;
//         align-items: flex-start;

//         .tweetText {
//           font-size: 24px;
//         }

//         .tweetCreatedAt {
//           color: #697882;
//         }

//         .tweetMedia {
//           display: grid;
//           grid-template-columns: auto auto;

//           .tweetImage {
//             border: 1px solid #e1e8ed;
//             border-radius: 5px;
//             width: 100%;
//           }
//         }
//       }

//       .tweetFooter {
//         display: flex;
//         justify-content: flex-start;

//         .retweets {
//           padding-left: 20px;
//         }
//       }
//     }
//   }

//   .favoritesContainer {
//     border: 4mm ridge #1da1f2;
//     width: 48%;
//   }
// }
</style>
