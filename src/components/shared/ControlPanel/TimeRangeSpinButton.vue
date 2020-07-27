<template>
  <div class="timeRangeSpinButton">
    <label :for="this.buttonId">{{ this.label }}</label>
    <b-form-spinbutton
      :min="this.min"
      :max="this.max"
      :id="this.buttonId"
      v-model="value"
      v-on:input="handleUpdate(value)"
      vertical
      :readonly="!featureEnabled"
    />
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";

const TimeRangeSpinButtonProps = Vue.extend({
  props: {
    min: String,
    max: String,
    buttonId: String,
    label: String,
    site: String
  }
});

@Component
export default class TimeRangeSpinButton extends TimeRangeSpinButtonProps {
  handleUpdate(value) {
    if (this.site === "Twitter") {
      store.dispatch(constants.UPDATE_TWITTER_TIME_RANGE, {
        ...store.state.twitter[constants.TWITTER_TIME_RANGE],
        [this.label]: value
      });
    } else if (this.site === "Reddit") {
      store.dispatch(constants.UPDATE_REDDIT_TIME_RANGE, {
        ...store.state.reddit[constants.REDDIT_TIME_RANGE],
        [this.label]: value
      });
    }
  }

  get featureEnabled() {
    return this.site === "Twitter"
      ? store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED]
      : store.state.reddit[constants.REDDIT_TIME_RANGE_ENABLED];
  }

  data() {
    return {
      value:
        this.site === "Twitter"
          ? store.state.twitter[constants.TWITTER_TIME_RANGE][this.label]
          : store.state.reddit[constants.REDDIT_TIME_RANGE][this.label]
    };
  }
}
</script>

<style lang="scss">
.timeRangeSpinButton {
  display: flex;
  flex-direction: column;
  width: 50px;
  margin-right: 10px;
  margin-left: 10px;
}
</style>
