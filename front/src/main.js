import Vue from 'vue'
import VueSocketIO from 'vue-socket.io'
import socketio from 'socket.io-client'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import App from './components/App.vue'


Vue.use(iView)

let apiUrl = "http://127.0.0.1:8002/";
if (process.env.NODE_ENV === "production") {
    apiUrl = "https://socketio.dovolopor.com"
}
Vue.use(new VueSocketIO({
    debug: true,
    connection: socketio(apiUrl)
}))

new Vue({
    el: '#app',
    render: h => h(App)
});
