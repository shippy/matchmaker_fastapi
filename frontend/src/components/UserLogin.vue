<template>
<div>
    <h1>User Login</h1>
    <form @submit.prevent="loginUser">
    <input v-model="username" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Login</button>
    </form>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores'

interface User {
    username: string;
    password: string;
}

interface TokenResponse {
    access_token: string;
    // Include other properties of the token response here
}

export default defineComponent({
data() {
    return {
    username: '',
    password: '',
    // Add a property to store the token
    token: null as string | null
    }
},
methods: {
    async loginUser() {
    try {
        // const user: User = { username: this.username, password: this.password }
        const response = await axios.post<TokenResponse>('/api/token', new URLSearchParams({
            'username': this.username,
            'password': this.password
        }))
        
        // Store the token in the user store
        const userStore = useUserStore()
        userStore.setToken(response.data.access_token)

        // Store the token in the component (TODO: Remove?)
        this.token = response.data.access_token

        // Clear the form fields after successful login
        this.username = ''
        this.password = ''
    } catch (err) {
        console.error(err)
    }
    }
}
})
</script>

<style>
/* Your styles here */
</style>