<template>
  <div v-if="loggedIn" class="controlPanelSection">
    <h1>
      Time Range
    </h1>
    <h4 id="time-range-tooltip-target">
      Save items in a certain time range.
      <b-icon icon="question-circle-fill" />
    </h4>
    <b-tooltip
      target="time-range-tooltip-target"
      triggers="hover"
      placement="bottom"
    >
      For example, entering in a time range of 3 hour means that
      {{ site === "Twitter" ? "tweets/favorites" : "comments/posts" }} made in
      the last 3 hours will not be deleted
    </b-tooltip>
    <div class="timeRangeSection">
      <div>
        <span>
          Enable/Disable
        </span>
        <b-form-checkbox
          switch
          id="timeRangeSwitch"
          v-on:change="handleTimeRangeSwitch()"
          :checked="checkIfTimeRangeSelected()"
        />
      </div>
      <div class="spinButtonContainer">
        <TimeRangeSpinButton
          min="0"
          max="23"
          buttonId="tr-hours"
          label="Hours"
          :site="site"
        />
        <TimeRangeSpinButton
          min="0"
          max="6"
          buttonId="tr-days"
          label="Days"
          :site="site"
        />
        <TimeRangeSpinButton
          min="0"
          max="51"
          buttonId="tr-weeks"
          label="Weeks"
          :site="site"
        />
        <TimeRangeSpinButton
          min="0"
          max="20"
          buttonId="tr-years"
          label="Years"
          :site="site"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";
import TimeRangeSpinButton from "@/components/shared/ControlPanel/TimeRangeSpinButton.vue";

const TimeRangeProps = Vue.extend({
  props: {
    site: String
  }
});

@Component({
  components: {
    TimeRangeSpinButton
  }
})
export default class TimeRange extends TimeRangeProps {
  get loggedIn() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_LOGGED_IN]
      : store.state.reddit[constants.REDDIT_LOGGED_IN];
  }

  handleTimeRangeSwitch() {
    if (this.site === "Twitter") {
      store.dispatch(
        constants.UPDATE_TWITTER_TIME_RANGE_ENABLED,
        store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED] !== true
      );
    } else if (this.site === "Reddit") {
      store.dispatch(
        constants.UPDATE_REDDIT_TIME_RANGE_ENABLED,
        store.state.reddit[constants.REDDIT_TIME_RANGE_ENABLED] !== true
      );
    }
  }

  checkIfTimeRangeSelected() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED]
      : store.state.reddit[constants.REDDIT_TIME_RANGE_ENABLED];
  }
}
</script>

<style lang="scss">
.controlPanelSection {
  width: 48%;
  border: 4mm ridge #939393;
  padding: 20px;
}

.timeRangeSection {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.spinButtonContainer {
  display: flex;
}
</style>
