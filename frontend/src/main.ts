import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import vue3GoogleLogin from "vue3-google-login"

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vue3GoogleLogin, {
    clientId: "987401178744-qqf2nn6btdaako4qmqlq92qhb0vfghcu.apps.googleusercontent.com",
})

app.mount('#app')
