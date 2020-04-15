<template>
  <div class="tweetsContainer" v-if="loggedIn">
    <h1>Your tweets</h1>
    <!-- <ul class="tweetList">
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
          <div class="tweetMedia" v-if="tweet.extended_entities && tweet.extended_entities.media">
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
    </ul> -->
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";

@Component
export default class UserTweetsPanel extends Vue {
  // loggedIn = false;

  // created() {
  //   console.log("component created!")
  //   this.loggedIn = store.state.twitterLoggedIn;
  // }

  // computed() {
  //   loggedIn: {
  //     return store.state.twitterLoggedIn;
  //   }
  // }

  // eslint-disable-next-line class-methods-use-this
  get loggedIn() {
    return store.state.twitterLoggedIn;
  }
}
</script>

<style lang="scss">
.tweetsContainer {
  width: 48%;
  border: 4mm ridge #1da1f2;

  .tweetList {
    padding-left: 0;
  }

  .tweet {
    padding: 15px;
    margin: 10px;
    border: 1px solid #e1e8ed;
    border-radius: 5px;
    list-style: none;

    &:hover {
      background-color: #dddddd;
    }

    .tweetHeader {
      display: flex;
      justify-content: flex-start;

      .tweetUsernames {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding-left: 5px;

        .tweetName {
          line-height: 1.3125;
          font-weight: bold;
        }
        .tweetUsername {
          color: #697882;
        }
      }
    }

    .tweetBody {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      .tweetText {
        font-size: 24px;
      }

      .tweetCreatedAt {
        color: #697882;
      }

      .tweetMedia {
        display: grid;
        grid-template-columns: auto auto;

        .tweetImage {
          border: 1px solid #e1e8ed;
          border-radius: 5px;
          width: 100%;
        }
      }
    }

    .tweetFooter {
      display: flex;
      justify-content: flex-start;

      .retweets {
        padding-left: 20px;
      }
    }
  }
}
</style>