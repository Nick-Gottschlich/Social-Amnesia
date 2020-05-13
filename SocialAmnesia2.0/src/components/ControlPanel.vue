<template>
  <div class="controlPanelContainer">
    <h1>
      Settings
    </h1>
  </div>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";

@Component
export default class ControlPanel extends Vue {}
</script>

<style lang="scss">
.controlPanelContainer {
  border: 4mm ridge #939393;
  padding: 20px;
}
</style>
