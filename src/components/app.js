
import Vue from 'vue';
import Vuetify from 'vuetify';
import JobApplication from './components/JobApplication.vue';

Vue.use(Vuetify);

const vuetify = new Vuetify();

new Vue({
  vuetify,
  el: '#app',
  components: {
    JobApplication
  },
  template: '<JobApplication/>'
});
