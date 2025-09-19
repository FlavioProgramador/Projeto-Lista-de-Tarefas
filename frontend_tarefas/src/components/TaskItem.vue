<script setup>
defineProps({
  tarefa: {
    type: Object,
    required: true
  }
});
</script>

<template>
  <li class="task-card">
    <div class="task-card-header">
      <h3 class="task-title">{{ tarefa.titulo }}</h3>
    </div>
    <p v-if="tarefa.descricao" class="task-description">{{ tarefa.descricao }}</p>
  </li>
</template>

<style scoped>
.task-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}
.task-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.task-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}
.task-description {
  color: #5a6e81;
  line-height: 1.5;
  margin-top: 0.5rem;
}
</style>