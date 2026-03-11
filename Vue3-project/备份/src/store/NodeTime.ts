import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNodeTimeStore = defineStore('NodeTime', () => {
  const currentYear = ref();

  function updateCurrentYear(year: number) {
    currentYear.value = year;
  }

  return {
    currentYear,
    updateCurrentYear
  }
})