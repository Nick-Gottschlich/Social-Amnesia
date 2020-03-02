<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <h2>wus poppin my g</h2>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <TestComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue';
import TestComponent from '@/components/TestComponent.vue';

export default {
  name: 'Home',
  components: {
    HelloWorld,
    TestComponent,
  },
};
</script>
