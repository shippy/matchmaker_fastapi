<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="questionnaire">
      <h2>{{ questionnaire.title }}</h2>
      <div v-for="question in questionnaire.questions" :key="`question-${question.id}`">
        <h3>{{ question.text }}</h3>
        <ul>
          <li v-for="answer in question.answers" :key="`answer-${answer.id}`">
            {{ answer.text }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
  
<script lang="ts">
import { defineComponent } from 'vue'
import { type RouteLocation } from "vue-router"
import axios from 'axios'
import Vue from 'vue'

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $route: RouteLocation;
  }
}

interface Answer {
  id: number;
  text: string;
}

interface Question {
  id: number;
  text: string;
  answers: Answer[];
}

interface Questionnaire {
  id: number;
  title: string;
  questions: Question[];
}

export default defineComponent({
  data() {
    return {
      questionnaire: null as Questionnaire | null,
      loading: true,
      error: null as string | null
    }
  },
  async created() {
    try {
      const response = await axios.get<Questionnaire>(`/api/questionnaire/${this.$route.params.id}`)
      this.questionnaire = response.data
      this.loading = false
    } catch (err: unknown) {
      this.error = (err as Error).message
      this.loading = false
    }
  }
})
</script>

<style>
/* Your styles here */
</style>
