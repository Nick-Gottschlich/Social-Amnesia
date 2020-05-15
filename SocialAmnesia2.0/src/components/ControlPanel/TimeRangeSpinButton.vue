<template>
  <div class="timeRangeSpinButton">
    <label :for="this.idProp">Hours</label>
    <b-form-spinbutton
      :min="this.min"
      :max="this.max"
      :id="this.idProp"
      v-model="value"
      v-on:input="handleUpdate(value)"
      vertical
    />
    <div>value {{ value }}</div>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";

const TimeRangeSpinButtonProps = Vue.extend({
  props: {
    min: Number,
    max: Number,
    idProp: String
  }
});

@Component
export default class TimeRangeSpinButton extends TimeRangeSpinButtonProps {
  handleUpdate(value) {
    // Update store from here
    console.log("value", value);
  }
}
</script>

<style lang="scss">
.timeRangeSpinButton {
  display: flex;
  flex-direction: column;
  width: 50px;
}
</style>
