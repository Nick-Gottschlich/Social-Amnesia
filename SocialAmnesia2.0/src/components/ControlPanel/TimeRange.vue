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
      tweets/favorites made in the last 3 hours will not be deleted
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
        />
        <TimeRangeSpinButton min="0" max="6" buttonId="tr-days" label="Days" />
        <TimeRangeSpinButton
          min="0"
          max="51"
          buttonId="tr-weeks"
          label="Weeks"
        />
        <TimeRangeSpinButton
          min="0"
          max="20"
          buttonId="tr-years"
          label="Years"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";
import TimeRangeSpinButton from "@/components/ControlPanel/TimeRangeSpinButton.vue";

@Component({
  components: {
    TimeRangeSpinButton
  }
})
export default class TimeRange extends Vue {
  get loggedIn() {
    return store.state.twitter[constants.TWITTER_LOGGED_IN];
  }

  handleTimeRangeSwitch() {
    store.dispatch(
      constants.UPDATE_TWITTER_TIME_RANGE_ENABLED,
      store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED] !== true
    );
  }

  checkIfTimeRangeSelected() {
    return store.state.twitter[constants.TWITTER_TIME_RANGE_ENABLED];
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
