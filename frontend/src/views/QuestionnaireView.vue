<template>
    <div>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else>
        <h1>{{ questionnaire.title }}</h1>
        <div v-for="question in questionnaire.questions" :key="`question-${question.id}`">
          <h2>{{ question.text }}</h2>
          <ul>
            <li v-for="answer in question.answers" :key="`answer-${answer.id}`">
              {{ answer.text }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        questionnaire: null,
        loading: true,
        error: null
      }
    },
    async created() {
      try {
        const response = await axios.get(`/api/questionnaires/${this.$route.params.id}`)
        this.questionnaire = response.data
        this.loading = false
      } catch (err) {
        this.error = err.message
        this.loading = false
      }
    }
  }
  </script>
  
  <style>
  /* Your styles here */
  </style>
  