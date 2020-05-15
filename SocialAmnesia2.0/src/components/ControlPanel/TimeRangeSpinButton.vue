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
    label: String
  }
});

@Component
export default class TimeRangeSpinButton extends TimeRangeSpinButtonProps {
  handleUpdate(value) {
    // Update store from here
    console.log("value", value);
  }

  get featureEnabled() {
    return store.state[constants.TWITTER_TIME_RANGE_ENABLED];
  }

  data() {
    return {
      value: 0
    };
  }
}
</script>

<style lang="scss">
.timeRangeSpinButton {
  display: flex;
  flex-direction: column;
  width: 50px;
  padding-right: 5px;
}
</style>
