<template>
  <div v-if="loggedIn" class="controlPanelSection">
    <h1>
      High Scores
    </h1>
    <h4 id="score-panel-tooltip-target">
      Save items that have gotten a certain amount of favorites (❤️'s) or
      retweets.
      <svg
        viewBox="0 0 515.556 515.556"
        xmlns="http://www.w3.org/2000/svg"
        class="questionSVG"
      >
        <path
          d="M257.778 0C115.641 0 0 115.641 0 257.778s115.641 257.778 257.778 257.778 257.778-115.641 257.778-257.778S399.914 0 257.778 0zM290 418.889h-64.444v-64.444H290zm32.222-147.769L290 303.342v18.88h-64.444V290c0-8.543 3.398-16.74 9.44-22.782l41.662-41.662c8.48-8.48 13.342-20.233 13.342-32.222 0-17.763-14.459-32.222-32.222-32.222s-32.222 14.459-32.222 32.222v32.222h-64.444v-32.222c0-53.305 43.361-96.667 96.667-96.667s96.667 43.361 96.667 96.667c-.001 29.39-11.44 57.018-32.224 77.786z"
        />
      </svg>
    </h4>
    <b-tooltip
      target="score-panel-tooltip-target"
      triggers="hover"
      placement="bottom"
    >
      For example, entering "100" for favorites will save any of your tweets
      that have gotten at least 100 favorites.
    </b-tooltip>
    <h6>
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
            Favorites
          </h5>
          <b-form-input
            type="number"
            aria-label="Favorites high score input"
            min="0"
            placeholder="Enter a number"
            v-model="favoritesValue"
            v-on:change="handleFavoritesScoreChange(favoritesValue)"
          ></b-form-input>
        </div>

        <div class="scoreInput">
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

@Component
export default class ScorePanel extends Vue {
  get loggedIn() {
    return store.state[constants.TWITTER_LOGGED_IN];
  }

  handleScorePanelSwitch() {
    store.dispatch(
      constants.UPDATE_TWITTER_SCORE_ENABLED,
      store.state[constants.TWITTER_SCORE_ENABLED] !== true
    );
  }

  checkIfScorePanelSelected() {
    return store.state[constants.TWITTER_SCORE_ENABLED];
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

  data() {
    return {
      favoritesValue: store.state[constants.TWITTER_FAVORITES_SCORE],
      retweetsValue: store.state[constants.TWITTER_RETWEETS_SCORE]
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

.questionSVG {
  position: relative;
  top: -2px;
  height: 20px;
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
