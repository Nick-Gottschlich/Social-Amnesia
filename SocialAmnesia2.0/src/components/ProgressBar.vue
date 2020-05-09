<template>
  <b-modal
    v-model="totalItems"
    title="Deleting your items..."
    centered
    no-close-on-backdrop
    no-close-on-esc
    hide-footer
    hide-header-close
  >
    <b-progress :max="totalItems" show-progress animated>
      <b-progress-bar :value="itemsDeleted">{{itemsDeleted}} / {{totalItems}}</b-progress-bar>
    </b-progress>
  </b-modal>
</template>

<script>
import { Component, Vue } from "vue-property-decorator";
import store from "@/store/index";
import constants from "@/store/constants";

@Component
export default class ProgressBar extends Vue {
  get totalItems() {
    return store.state[constants.CURRENTLY_DELETING].totalItems;
  }

  get itemsDeleted() {
    return store.state[constants.CURRENTLY_DELETING].itemsDeleted;
  }
}
</script>