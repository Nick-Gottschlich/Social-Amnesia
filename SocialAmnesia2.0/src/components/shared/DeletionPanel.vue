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
  deleteTwitterItems(items, itemString, whitelistedItems) {
    const itemInSavedTimeRange = item => {
      const timeRangeObject = store.state.twitter[constants.TWITTER_TIME_RANGE];

      const hoursBackToSave =
        timeRangeObject.Hours +
        timeRangeObject.Days * 24 +
        timeRangeObject.Weeks * 168 +
        timeRangeObject.Years * 8766;
      const dateOfHoursBackToSave = new Date();
      dateOfHoursBackToSave.setHours(
        dateOfHoursBackToSave.getHours() - hoursBackToSave
      );

      return (
        new Date(item.created_at) >
        new Date(dateOfHoursBackToSave.toGMTString())
      );
    };

    const itemLowerThanScore = item => {
      if (
        item.favorite_count >=
        store.state.twitter[constants.TWITTER_FAVORITES_SCORE]
      ) {
        return false;
      }

      if (
        item.retweet_count >=
        store.state.twitter[constants.TWITTER_RETWEETS_SCORE]
      ) {
        return false;
      }

      return true;
    };

    if (
      window.confirm(
        `Are you sure you want to delete your ${itemString}? THIS ACTION IS PERMANENT!`
      )
    ) {
      const promiseArray = [];

      const shouldDeleteItem = item => {
        const itemIsWhitelisted = whitelistedItems[`${itemString}-${item.id}`];

        const shouldDelete =
          !itemIsWhitelisted &&
          (!itemInSavedTimeRange(item) ||
            !store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED]) &&
          (itemString === "favorites" ||
            itemLowerThanScore(item) ||
            !store.state.twitter[constants.TWITTER_SCORE_ENABLED]);

        return shouldDelete;
      };

      const totalItemsLength = items.filter(item => {
        return shouldDeleteItem(item);
      }).length;

      store.dispatch(constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED);
      store.dispatch(
        constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS,
        totalItemsLength
      );

      items.forEach(item => {
        if (shouldDeleteItem(item)) {
          promiseArray.push(
            store.state.twitter[constants.TWITTER_USER_CLIENT]
              .post(
                itemString === "tweets"
                  ? "statuses/destroy"
                  : "favorites/destroy",
                {
                  id: item.id_str
                }
              )
              .then(() => {
                store.commit(
                  constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED
                );
              })
              .catch(error => {
                console.log(
                  `Failed to delete item with error: ${JSON.stringify(error)}`
                );
              })
          );
        }
      });

      Promise.allSettled(promiseArray).then(() => {
        helpers.twitterGatherAndSetItems({
          apiRoute:
            itemString === "tweets"
              ? constants.TWEETS_ROUTE
              : constants.FAVORITES_ROUTE,
          itemArray: []
        });

        setTimeout(() => {
          store.dispatch(constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS, 0);
        }, 2500);
      });
    }
  }

  handleDeleteTwitterTweets() {
    this.deleteTwitterItems(
      store.state.twitter[constants.USER_TWEETS],
      "twitter tweets",
      store.state.twitter[constants.WHITELISTED_TWEETS]
    );
  }

  handleDeleteFavorites() {
    this.deleteTwitterItems(
      store.state.twitter[constants.USER_FAVORITES],
      "twitter favorites",
      store.state.twitter[constants.WHITELISTED_FAVORITES]
    );
  }

  deleteRedditItems(items, itemString, whitelistedItems) {
    const redditItemInSavedTimeRange = item => {
      const timeRangeObject = store.state.reddit[constants.REDDIT_TIME_RANGE];

      const hoursBackToSave =
        timeRangeObject.Hours +
        timeRangeObject.Days * 24 +
        timeRangeObject.Weeks * 168 +
        timeRangeObject.Years * 8766;
      const dateOfHoursBackToSave = new Date();
      dateOfHoursBackToSave.setHours(
        dateOfHoursBackToSave.getHours() - hoursBackToSave
      );

      const convertedItemDate = new Date(
        new Date(item.data.created_utc * 1000).toGMTString()
      );
      const convertedDateRangeDate = new Date(
        dateOfHoursBackToSave.toGMTString()
      );
      return convertedItemDate > convertedDateRangeDate;
    };

    const redditItemLowerThanScore = item => {
      if (
        item.data.score >= store.state.reddit[constants.REDDIT_UPVOTES_SCORE]
      ) {
        return false;
      }

      return true;
    };

    if (
      window.confirm(
        `Are you sure you want to delete your ${itemString}? THIS ACTION IS PERMANENT!`
      )
    ) {
      const promiseArray = [];

      const shouldDeleteItem = item => {
        const itemIsWhitelisted =
          whitelistedItems[`${itemString}-${item.data.name}`];

        const shouldDelete =
          !itemIsWhitelisted &&
          (!redditItemInSavedTimeRange(item) ||
            !store.state.reddit[constants.REDDIT_TIME_RANGE_ENABLED]) &&
          (redditItemLowerThanScore(item) ||
            !store.state.reddit[constants.REDDIT_SCORE_ENABLED]);

        return shouldDelete;
      };

      const totalItemsLength = items.filter(item => {
        return shouldDeleteItem(item);
      }).length;

      store.dispatch(constants.RESET_CURRENTLY_DELETING_ITEMS_DELETED);
      store.dispatch(
        constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS,
        totalItemsLength
      );

      items.forEach(item => {
        if (shouldDeleteItem(item)) {
          promiseArray.push(
            helpers
              .makeRedditPostRequest(
                "https://oauth.reddit.com/api/editusertext/",
                {
                  thing_id: item.data.name,
                  text: helpers.generateRandomText()
                }
              )
              .then(() => {
                helpers
                  .makeRedditPostRequest("https://oauth.reddit.com/api/del/", {
                    id: item.data.name
                  })
                  .then(() => {
                    store.commit(
                      constants.INCREMENT_CURRENTLY_DELETING_ITEMS_DELETED
                    );
                  })
                  .catch(error => {
                    console.log(
                      `Failed to delete item with error: ${JSON.stringify(
                        error
                      )}`
                    );
                  });
              })
              .catch(error => {
                console.log(
                  `Failed to edit item with error: ${JSON.stringify(error)}`
                );
              })
          );
        }
      });

      Promise.allSettled(promiseArray).then(() => {
        helpers.redditGatherAndSetItems();

        setTimeout(() => {
          store.dispatch(constants.UPDATE_CURRENTLY_DELETING_TOTAL_ITEMS, 0);
        }, 2500);
      });
    }
  }

  handleDeleteRedditComments() {
    this.deleteRedditItems(
      store.state.reddit[constants.REDDIT_COMMENTS],
      "reddit comments",
      store.state.reddit[constants.REDDIT_WHITELISTED_COMMENTS]
    );
  }

  handleDeleteRedditPosts() {
    this.deleteRedditItems(
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
