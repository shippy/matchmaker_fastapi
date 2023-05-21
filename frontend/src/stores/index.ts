import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null as string | null,
  }),
  actions: {
    setToken(token: string) {
      this.token = token;
    },
  },
})
// export const variable = 1;