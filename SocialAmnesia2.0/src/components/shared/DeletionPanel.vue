<template>
  <div class="deletionPanelSurroundingContainer" v-if="loggedIn">
    <div class="deletionPanelContainer">
      <h1>Clean {{ site }}</h1>
      <div class="deletionButtonContainer">
        <b-button
          class="deletionButton"
          variant="danger"
          v-on:click="
            site === 'Twitter'
              ? handleDeleteTwitterTweets()
              : handleDeleteRedditComments()
          "
        >
          Click to delete {{ site === "Twitter" ? "tweets" : "comments" }}
        </b-button>
        <b-button
          variant="danger"
          v-on:click="
            site === 'Twitter'
              ? handleDeleteTwitterFavorites()
              : handleDeleteRedditPosts()
          "
        >
          Click to delete
          {{ site === "Twitter" ? "❤️'s (favorites)" : "posts" }}
        </b-button>
      </div>
    </div>
    <div class="deletionPanelContainer">
      <h1>
        Schedule Daily Clean
      </h1>
      <div class="switchAndTimeContainer">
        <div class="switchesContainer">
          <div class="textAndSwitchContainer">
            <span>
              Schedule {{ site === "Twitter" ? "tweets" : "comments" }} deletion
              <b-icon
                icon="question-circle-fill"
                id="schedule-delete-first-target"
              />
            </span>
            <b-tooltip
              target="schedule-delete-first-target"
              triggers="hover"
              placement="bottom"
            >
              This will clean your
              {{ site === "Twitter" ? "tweets" : "comments" }} daily at the time
              specified.
            </b-tooltip>
            <b-form-checkbox
              switch
              id="scheduleDeletionSwitchFirst"
              v-on:change="
                handleScheduleDeletionSwitch(
                  site === 'Twitter' ? 'tweets' : 'comments'
                )
              "
              :checked="
                checkIfScheduleDeletionSelected(
                  site === 'Twitter' ? 'tweets' : 'comments'
                )
              "
            />
          </div>
          <div class="textAndSwitchContainer">
            <span>
              Schedule {{ site === "Twitter" ? "favorites" : "posts" }} deletion
              <b-icon
                icon="question-circle-fill"
                id="schedule-delete-second-target"
              />
            </span>
            <b-tooltip
              target="schedule-delete-second-target"
              triggers="hover"
              placement="bottom"
            >
              This will clean your
              {{ site === "Twitter" ? "favorites" : "posts" }} daily at the time
              specified.
            </b-tooltip>
            <b-form-checkbox
              switch
              id="scheduleDeletionSwitchSecond"
              v-on:change="
                handleScheduleDeletionSwitch(
                  site === 'Twitter' ? 'favorites' : 'posts'
                )
              "
              :checked="
                checkIfScheduleDeletionSelected(
                  site === 'Twitter' ? 'favorites' : 'posts'
                )
              "
            />
          </div>
        </div>
        <b-time
          v-model="value"
          locale="en"
          @context="onContext"
          :readonly="!scheduleEnabled"
        ></b-time>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-alert */
/* eslint-disable @typescript-eslint/camelcase */
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";
import helpers from "@/util/helpers";

const DeletionPanelProps = Vue.extend({
  props: {
    site: String
  }
});

@Component
export default class DeletionPanel extends DeletionPanelProps {
  handleDeleteTwitterTweets() {
    helpers.deleteTwitterItems(
      store.state.twitter[constants.USER_TWEETS],
      "twitter tweets",
      store.state.twitter[constants.WHITELISTED_TWEETS]
    );
  }

  handleDeleteTwitterFavorites() {
    helpers.deleteTwitterItems(
      store.state.twitter[constants.USER_FAVORITES],
      "twitter favorites",
      store.state.twitter[constants.WHITELISTED_FAVORITES]
    );
  }

  handleDeleteRedditComments() {
    helpers.deleteRedditItems(
      store.state.reddit[constants.REDDIT_COMMENTS],
      "reddit comments",
      store.state.reddit[constants.REDDIT_WHITELISTED_COMMENTS]
    );
  }

  handleDeleteRedditPosts() {
    helpers.deleteRedditItems(
      store.state.reddit[constants.REDDIT_POSTS],
      "reddit posts",
      store.state.reddit[constants.REDDIT_WHITELISTED_POSTS]
    );
  }

  handleScheduleDeletionSwitch(key) {
    if (this.site === "Twitter") {
      const obj = {
        ...store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED],
        [key]: !store.state.twitter[
          constants.TWITTER_SCHEDULE_DELETION_ENABLED
        ][key]
      };

      store.dispatch(constants.UPDATE_TWITTER_SCHEDULE_DELETION_ENABLED, obj);
    } else if (this.site === "Reddit") {
      const obj = {
        ...store.state.reddit[constants.REDDIT_SCHEDULE_DELETION_ENABLED],
        [key]: !store.state.reddit[constants.REDDIT_SCHEDULE_DELETION_ENABLED][
          key
        ]
      };

      store.dispatch(constants.UPDATE_REDDIT_SCHEDULE_DELETION_ENABLED, obj);
    }
  }

  checkIfScheduleDeletionSelected(key) {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED][key]
      : store.state.reddit[constants.REDDIT_SCHEDULE_DELETION_ENABLED][key];
  }

  onContext(context) {
    if (this.site === "Twitter") {
      store.dispatch(constants.UPDATE_TWITTER_SCHEDULE_TIME, context.value);
    } else if (this.site === "Reddit") {
      store.dispatch(constants.UPDATE_REDDIT_SCHEDULE_TIME, context.value);
    }
  }

  get loggedIn() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_LOGGED_IN]
      : store.state.reddit[constants.REDDIT_LOGGED_IN];
  }

  get scheduleEnabled() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED]
          .tweets ||
          store.state.twitter[constants.TWITTER_SCHEDULE_DELETION_ENABLED]
            .favorites
      : store.state.reddit[constants.REDDIT_SCHEDULE_DELETION_ENABLED]
          .comments ||
          store.state.reddit[constants.REDDIT_SCHEDULE_DELETION_ENABLED].posts;
  }

  data() {
    return {
      value:
        this.site === "Twitter"
          ? store.state.twitter[constants.TWITTER_SCHEDULE_TIME]
          : store.state.reddit[constants.REDDIT_SCHEDULE_TIME]
    };
  }
}
</script>

<style lang="scss">
.deletionPanelSurroundingContainer {
  display: flex;
}

.deletionPanelContainer {
  border: 4mm ridge #dc3545;
  padding: 20px;
  margin-top: 10px;
  margin-right: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.deletionButtonContainer {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.deletionButton {
  margin-bottom: 5px;
}

.switchAndTimeContainer {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}

.textAndSwitchContainer {
  display: flex;
  flex-direction: column;
  padding-right: 20px;
  padding-bottom: 20px;
}
</style>
