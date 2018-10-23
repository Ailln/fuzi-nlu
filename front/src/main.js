import Vue from 'vue';
import App from './components/App.vue';

import iView from 'iview';
import 'iview/dist/styles/iview.css';

Vue.use(iView);

new Vue({
    el: '#app',
    render: h => h(App)
});
