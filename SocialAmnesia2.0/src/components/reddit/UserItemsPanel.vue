<template>
  <div class="redditUserItemsContainer">
    <h1>{{ this.itemtype === "comments" ? "Your comments" : "Your posts" }}</h1>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="itemList"
      align="center"
    />
    <ul id="redditItemsList" class="tweetList">
      <li v-for="item in userItems" :key="`${itemtype}-${item.data.id}`">
        <div class="redditItemAndOptionsContainer">
          <div class="redditOptions">
            <div class="redditWhiteList">
              <b-form-checkbox
                switch
                :id="`checklist-${itemtype}-${item.data.id}`"
              />
              <span>Whitelist</span>
            </div>
            <div class="redditDeleteIconContainer">
              <b-icon
                v-b-tooltip.hover.bottom
                :title="
                  itemtype === 'comments'
                    ? 'Delete this comment'
                    : 'Delete this post'
                "
                icon="trash"
                class="tweetDeleteIcon"
              />
            </div>
          </div>
          <a
            class="redditItem"
            :href="`https://reddit.com${item.data.permalink}`"
            target="_blank"
            @click.prevent="openExternalBrowser"
          >
            <div class="redditTitleContainer">
              <span class="redditLinkTitle">
                <a
                  :href="
                    itemtype === 'comments'
                      ? item.data.link_url
                      : `https://reddit.com${item.data.permalink}`
                  "
                  target="_blank"
                  @click.prevent="openExternalBrowser"
                >
                  {{
                    itemtype === "comments"
                      ? item.data.link_title
                      : item.data.title
                  }}
                </a>
              </span>
              <div class="redditSubPostedTo">
                <span>in</span>
                <a
                  :href="
                    `https://reddit.com/${item.data.subreddit_name_prefixed}`
                  "
                  target="_blank"
                  @click.prevent="openExternalBrowser"
                >
                  {{ item.data.subreddit_name_prefixed }}
                </a>
              </div>
            </div>
            <div class="redditPostContentContainer">
              <div class="redditUserAndScore">
                <span class="redditUser">
                  {{ item.data.author }}
                </span>
                <span class="redditPostScore">
                  {{ item.data.score }}
                  {{ item.data.score === 1 ? "point" : "points" }}
                </span>
                <span class="redditPostDate">
                  {{ new Date(item.data.created_utc * 1000).toDateString() }}
                </span>
              </div>
              <span class="redditItemBody">
                {{ createRedditItemBody(item) }}
              </span>
            </div>
          </a>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";
import helpers from "@/util/helpers";
import remote from "electron";

const UserItemsPanelProps = Vue.extend({
  props: {
    itemtype: String
  }
});

@Component
export default class UserItemsPanel extends UserItemsPanelProps {
  currentPage = 1;

  perPage = 5;

  get userItems() {
    console.log("comments", store.state.reddit[constants.REDDIT_COMMENTS]);
    console.log("posts", store.state.reddit[constants.REDDIT_POSTS]);

    if (this.itemtype === "comments") {
      return store.state.reddit[constants.REDDIT_COMMENTS].slice(
        (this.currentPage - 1) * this.perPage,
        this.currentPage * this.perPage
      );
    }
    if (this.itemtype === "posts") {
      return store.state.reddit[constants.REDDIT_POSTS].slice(
        (this.currentPage - 1) * this.perPage,
        this.currentPage * this.perPage
      );
    }
    return [];
  }

  get rows() {
    if (this.itemtype === "comments") {
      return store.state.twitter[constants.USER_TWEETS].length;
    }
    if (this.itemtype === "posts") {
      return store.state.twitter[constants.USER_FAVORITES].length;
    }
    return 0;
  }

  createRedditItemBody(item) {
    const text =
      this.itemtype === "comments" ? item.data.body : item.data.selftext;

    return text.length >= 500 ? `${text.slice(0, 500)}...` : text;
  }

  openExternalBrowser(event) {
    remote.shell.openExternal(event.target.href);
  }
}
</script>

<style lang="scss">
.redditUserItemsContainer {
  width: 48%;
  height: 99%;
  border: 4mm ridge #1da1f2;
  margin-bottom: 10px;
}

.redditItemsList {
  padding-left: 0;
  list-style: none;
}

.redditItemAndOptionsContainer {
  display: flex;
  align-items: center;
}

.redditOptions {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.redditWhitelist {
  display: flex;
  padding-left: 5px;
  padding-bottom: 20px;
}

.redditItem {
  padding: 15px;
  margin: 10px;
  border: 1px solid #e1e8ed;
  border-radius: 5px;
  flex-grow: 1;
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  text-decoration: inherit;
  color: inherit;

  &:hover {
    background-color: #dddddd;
    text-decoration: inherit;
    color: inherit;
  }
}

.redditTitleContainer {
  display: flex;
  align-items: center;
}

.redditLinkTitle {
  color: #0000ff;
}

.redditSubPostedTo {
  padding-left: 10px;
  font-size: 13px;
}

.redditUser {
  background-color: #0055df;
  color: #ffffff;
  font-weight: bold;
  padding: 0 2px 0 2px;
  border-radius: 3px;
  font-size: 14px;
}

.redditPostContentContainer {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-left: 20px;
}

.redditPostScore {
  padding-left: 10px;
  font-weight: bold;
  font-size: 14px;
}

.redditPostDate {
  color: #888;
  font-size: 13px;
  padding-left: 5px;
}

.redditItemBody {
  padding-top: 10px;
  text-align: left;
  word-break: break-word;
  white-space: pre-line;
}
</style>
