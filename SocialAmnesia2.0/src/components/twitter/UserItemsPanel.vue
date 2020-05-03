<template>
  <div class="tweetsContainer" v-if="loggedIn">
    <h1>{{this.itemType === "tweets" ? "Your tweets" : "Your favorites"}}</h1>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="itemList"
      align="center"
    />
    <ul id="itemList" class="tweetList">
      <li class="itemsList" v-for="tweet in userItems" :key="`${itemType}-${tweet.id}`">
        <div class="tweetAndOptionsContainer">
          <div class="tweetOptions">
            <b-form-checkbox
              switch
              :id="`checklist-${itemType}-${tweet.id}`"
              v-on:change="handleChanged(tweet)"
              :checked="checkIfSelected(tweet)"
            />
            <span>Whitelist</span>
          </div>
          <div class="tweet">
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
                <li v-for="media in tweet.extended_entities.media" :key="media.id">
                  <img
                    v-if="media.type === 'photo'"
                    class="tweetContent"
                    :src="media.media_url_https"
                  />
                  <video
                    v-if="media.type === 'video' || media.type === 'animated_gif'"
                    controls
                    class="tweetContent"
                  >
                    <source
                      :src="media.video_info && media.video_info.variants[0].url"
                      type="video/mp4"
                    />
                  </video>
                </li>
              </div>
              <span class="tweetCreatedAt">{{new Date(tweet.created_at).toLocaleString()}}</span>
            </div>
            <div class="tweetFooter">
              <div class="favorites">❤️{{tweet.favorite_count}}</div>
              <div class="retweets">🔁{{tweet.retweet_count}}</div>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable class-methods-use-this */
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";

const UserItemsPanelProps = Vue.extend({
  props: {
    itemType: String
  }
});

@Component
export default class UserItemsPanel extends UserItemsPanelProps {
  currentPage = 1;

  perPage = 5;

  itemType = this.itemType;

  checkIfSelected(tweet) {
    return this.itemType === "tweets"
      ? store.state[constants.WHITELISTED_TWEETS][`tweets-${tweet.id}`]
      : store.state[constants.WHITELISTED_FAVORITES][`favorites-${tweet.id}`];
  }

  handleChanged(item) {
    if (this.itemType === "tweets") {
      store.dispatch(constants.UPDATE_WHITELISTED_TWEETS, `tweets-${item.id}`);
    } else if (this.itemType === "favorites") {
      store.dispatch(
        constants.UPDATE_WHITELISTED_FAVORITES,
        `favorites-${item.id}`
      );
    }
  }

  get loggedIn() {
    return store.state[constants.TWITTER_LOGGED_IN];
  }

  get userItems() {
    if (this.itemType === "tweets") {
      return store.state[constants.USER_TWEETS].slice(
        (this.currentPage - 1) * this.perPage,
        this.currentPage * this.perPage
      );
    }
    if (this.itemType === "favorites") {
      return store.state[constants.USER_FAVORITES].slice(
        (this.currentPage - 1) * this.perPage,
        this.currentPage * this.perPage
      );
    }
    return [];
  }

  get rows() {
    if (this.itemType === "tweets") {
      return store.state[constants.USER_TWEETS].length;
    }
    if (this.itemType === "favorites") {
      return store.state[constants.USER_FAVORITES].length;
    }
    return 0;
  }
}
</script>

<style lang="scss">
.tweetsContainer {
  width: 48%;
  height: 99%;
  border: 4mm ridge #1da1f2;
  margin-bottom: 10px;

  .tweetList {
    padding-left: 0;
    list-style: none;
  }

  .tweetAndOptionsContainer {
    display: flex;
    align-items: center;

    .tweetOptions {
      display: flex;
      padding-left: 5px;
    }

    .tweet {
      padding: 15px;
      margin: 10px;
      border: 1px solid #e1e8ed;
      border-radius: 5px;
      flex-grow: 1;

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

          .tweetContent {
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
}
</style>