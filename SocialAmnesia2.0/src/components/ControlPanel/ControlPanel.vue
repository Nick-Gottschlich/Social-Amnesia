<template>
  <div v-if="loggedIn" class="controlPanelSection">
    <h1>
      Time Range
    </h1>
    <h4>
      Enter in the time range of tweets you would like to save.
    </h4>
    <h5>
      For example, entering in a time range of 3 hour means that
      tweets/favorites made in the last 3 hours will not be deleted
    </h5>
    <div class="timeRangeSection">
      <div>
        <span>
          Enable or disable this feature:
        </span>
        <b-form-checkbox
          switch
          id="timeRangeSwitch"
          v-on:change="handleTimeRangeSwitch()"
          :checked="checkIfTimeRangeSelected()"
        />
      </div>
      <TimeRangeSpinButton
        min="0"
        max="23"
        buttonId="time-range-hours"
        label="Hours"
      />
      <TimeRangeSpinButton
        min="0"
        max="6"
        buttonId="time-range-days"
        label="Days"
      />
      <TimeRangeSpinButton
        min="0"
        max="51"
        buttonId="time-range-weeks"
        label="Weeks"
      />
      <TimeRangeSpinButton
        min="0"
        max="20"
        buttonId="time-range-years"
        label="Years"
      />
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
export default class ControlPanel extends Vue {
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
  width: 50%;
  border: 4mm ridge #939393;
  padding: 20px;
}

.timeRangeSection {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
</style>
