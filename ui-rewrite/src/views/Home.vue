<template>
  <div class="home">
    <TestComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import TestComponent from '@/components/TestComponent.vue';

export default {
  name: 'Home',
  components: {
    TestComponent,
  },
};
</script>
