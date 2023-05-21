<template>
    <div>
      <h1>User Registration</h1>
      <form @submit.prevent="registerUser">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue'
  import axios from 'axios'
  
  interface User {
    email: string;
    password: string;
  }
  
  export default defineComponent({
    data() {
      return {
        email: '',
        password: '',
      }
    },
    methods: {
      async registerUser() {
        try {
          const user: User = { email: this.email, password: this.password }
          await axios.post('/api/events/create_user', user)
          // Clear the form fields after successful registration
          this.email = ''
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
  