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
    <div class="timeRange">
      <TimeRangeSpinButton min="0" max="23" idProp="time-range-hours" />
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
}
</script>

<style lang="scss">
.controlPanelSection {
  border: 4mm ridge #939393;
  padding: 20px;
}

.timeRangeSection {
  display: flex;
  flex-direction: column;
  width: 50px;
}
</style>
