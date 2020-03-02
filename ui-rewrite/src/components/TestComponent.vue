<template>
  <div id="test">
    {{ message }}
    TEST
    {{data}}
  </div>
</template>

<script>
import { Component, Prop, Vue } from 'vue-property-decorator';
import axios from 'axios';

// const test = new Vue({
//   el: '#test',
//   data: {
//     message: 'wut',
//   },
// });

@Component
export default class Test extends Vue {
  message = 'what up g';

  data = ''

  render() {
    axios.get('https://jsonplaceholder.typicode.com/todos/1')
      .then((data) => {
        this.data = data;
      });

    console.log('data');
  }
}
</script>
