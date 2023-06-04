<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="questionnaire">
      <h2>{{ questionnaire.title }}</h2>
      <FormKit type="form" v-for="question in questionnaire.questions" :key="question.id">
        <FormKit
          type="radio"
          :label="question.text"
          :name="'question_' + question.id"
          :options="question.answers.reduce((obj, answer) => ({ ...obj, [answer.id]: answer.text }), {})"
        />
      </FormKit>
    </div>
  </div>
</template>
  
<script lang="ts">
import { defineComponent } from 'vue'
import { type RouteLocation } from "vue-router"
import axios from 'axios'
import Vue from 'vue'
// import FormKit from '@formkit/vue'

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

interface Response {
  respondent_id: number;
  answer_id: number;
  // Include other properties of Response here
}

export default defineComponent({
  data() {
    return {
      questionnaire: null as Questionnaire | null,
      loading: true,
      error: null as string | null,
      respondentId: null as number | null
    }
  },
  async created() {
    try {
      const response = await axios.get<Questionnaire>(`http://localhost:8000/questionnaire/${this.$route.params.id}`)
      this.questionnaire = response.data
      this.loading = false
    } catch (err: unknown) {
      this.error = (err as Error).message
      this.loading = false
    }
  },
  methods: {
    async createResponse(answerId: number) {
      try {
        const response = await axios.post<Response>('/api/events/create_response', {
          answer_id: answerId,
          respondent_id: this.respondentId // Include respondentId in the request
        })
        this.respondentId = response.data.respondent_id // Store the respondent_id for future requests
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
