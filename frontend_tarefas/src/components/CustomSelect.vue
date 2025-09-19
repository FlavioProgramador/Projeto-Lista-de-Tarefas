<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  },
  options: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);

const selectOption = (option) => {
  emit('update:modelValue', option);
  isOpen.value = false;
};
</script>

<template>
  <div class="custom-select" @mouseleave="isOpen = false">
    <button class="select-button" @click="isOpen = !isOpen">
      <span>{{ modelValue }}</span>
      <svg class="arrow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
    <transition name="fade">
      <ul v-if="isOpen" class="options-list">
        <li
          v-for="option in options"
          :key="option"
          @click="selectOption(option)"
          :class="{ selected: option === modelValue }"
        >
          {{ option }}
        </li>
      </ul>
    </transition>
  </div>
</template>

<style scoped>
.custom-select {
  position: relative;
  width: 125px;
  font-size: 0.9rem;
}

.select-button {
  width: 100%;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #2c3e50;
  font-family: inherit;
  font-size: inherit;
}

.select-button:hover {
  border-color: #aaa;
}

.arrow {
  width: 16px;
  height: 16px;
  color: #888;
}

.options-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  list-style: none;
  padding: 0.5rem 0;
  margin-top: 0.25rem;
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.options-list li {
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: #2c3e50;
}

.options-list li:hover {
  background-color: #f0f0f0;
}

.options-list li.selected {
  background-color: #eaf3fe;
  font-weight: 600;
  color: var(--color-primary, #4a90e2);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>