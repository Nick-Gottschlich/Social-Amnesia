<template>
  <div v-if="loggedIn" class="controlPanelSection">
    <h1>
      Time Range
    </h1>
    <h4 id="time-range-tooltip-target">
      Save items in a certain time range.
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
    return store.state[constants.TWITTER_LOGGED_IN];
  }

  handleTimeRangeSwitch() {
    store.dispatch(
      constants.UPDATE_TWITTER_TIME_RANGE_ENABLED,
      store.state[constants.TWITTER_TIME_RANGE_ENABLED] !== true
    );
  }

  checkIfTimeRangeSelected() {
    return store.state[constants.TWITTER_TIME_RANGE_ENABLED];
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

.questionSVG {
  position: relative;
  top: -2px;
  height: 20px;
}

.spinButtonContainer {
  display: flex;
}
</style>
