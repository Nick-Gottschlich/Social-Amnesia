<template>
  <div v-if="loggedIn" class="controlPanelSection">
    <h1>
      High Scores
    </h1>
    <h4 id="score-panel-tooltip-target">
      {{
        `Save items that have gotten a certain amount of ${
          site === "Twitter" ? "favorites (❤️s) or retweets." : "upvotes."
        }`
      }}
      <b-icon icon="question-circle-fill" />
    </h4>
    <b-tooltip
      target="score-panel-tooltip-target"
      triggers="hover"
      placement="bottom"
    >
      {{
        site === "Twitter"
          ? 'For example, entering "100" for favorites will save any of your tweets that have gotten at least 100 favorites.'
          : 'For example, entering "100" will save any comment or post that has at least 100 upvotes'
      }}
    </b-tooltip>
    <h6 v-if="site === 'Twitter'">
      This setting only affects the "tweets" section below.
    </h6>
    <div class="inputSection">
      <div class="scorePanelSwitchContainer">
        <span>
          Enable/Disable
        </span>
        <b-form-checkbox
          switch
          id="scorePanelSwitch"
          v-on:change="handleScorePanelSwitch()"
          :checked="checkIfScorePanelSelected()"
        />
      </div>
      <div class="scoreInputsContainer">
        <div class="scoreInput">
          <h5>
            {{ site === "Twitter" ? "Favorites" : "Upvotes" }}
          </h5>
          <b-form-input
            type="number"
            aria-label="Favorites high score input"
            min="0"
            placeholder="Enter a number"
            :v-model="site === 'Twitter' ? favoritesValue : upvotesValue"
            v-on:change="
              site === 'Twitter'
                ? handleFavoritesScoreChange(favoritesOrUpvotesValue)
                : handleUpvotesScoreChange(favoritesOrUpvotesValue)
            "
            :disabled="!featureEnabled"
          ></b-form-input>
        </div>

        <div class="scoreInput" v-if="site === 'Twitter'">
          <h5>
            Retweets
          </h5>
          <b-form-input
            type="number"
            aria-label="Favorites high score input"
            min="0"
            placeholder="Enter a number"
            v-model="retweetsValue"
            v-on:change="handleRetweetsScoreChange(retweetsValue)"
            :disabled="!featureEnabled"
          ></b-form-input>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";

const ScorePanelProps = Vue.extend({
  props: {
    site: String
  }
});

@Component
export default class ScorePanel extends ScorePanelProps {
  get loggedIn() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_LOGGED_IN]
      : store.state.reddit[constants.REDDIT_LOGGED_IN];
  }

  get featureEnabled() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_SCORE_ENABLED]
      : store.state.reddit[constants.REDDIT_SCORE_ENABLED];
  }

  handleScorePanelSwitch() {
    if (this.site === "Twitter") {
      store.dispatch(
        constants.UPDATE_TWITTER_SCORE_ENABLED,
        store.state.twitter[constants.TWITTER_SCORE_ENABLED] !== true
      );
    } else if (this.site === "Reddit") {
      store.dispatch(
        constants.UPDATE_REDDIT_SCORE_ENABLED,
        store.state.reddit[constants.REDDIT_SCORE_ENABLED] !== true
      );
    }
  }

  checkIfScorePanelSelected() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_SCORE_ENABLED]
      : store.state.reddit[constants.REDDIT_SCORE_ENABLED];
  }

  handleFavoritesScoreChange(favoritesValue) {
    store.dispatch(
      constants.UPDATE_TWITTER_FAVORITES_SCORE,
      Math.floor(favoritesValue) || 0
    );
  }

  handleRetweetsScoreChange(retweetsValue) {
    store.dispatch(
      constants.UPDATE_TWITTER_RETWEETS_SCORE,
      Math.floor(retweetsValue) || 0
    );
  }

  handleUpvotesScoreChange(upvotesValue) {
    store.dispatch(
      constants.UPDATE_REDDIT_UPVOTES_SCORE,
      Math.floor(upvotesValue) || 0
    );
  }

  data() {
    return {
      favoritesValue: store.state.twitter[constants.TWITTER_FAVORITES_SCORE],
      retweetsValue: store.state.twitter[constants.TWITTER_RETWEETS_SCORE],
      upvotesValue: store.state.reddit[constants.REDDIT_UPVOTES_SCORE]
    };
  }
}
</script>

<style lang="scss">
.controlPanelSection {
  width: 48%;
  border: 4mm ridge #939393;
  padding: 20px;
}

.inputSection {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.scoreInputsContainer {
  display: flex;
}

.scoreInput {
  margin-left: 10px;
  margin-right: 10px;
}

.scorePanelSwitchContainer {
  flex-basis: 10%;
}
</style>
