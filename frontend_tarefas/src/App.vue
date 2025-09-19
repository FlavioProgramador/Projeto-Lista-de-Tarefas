<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import TaskItem from './components/TaskItem.vue';

const API_URL = 'http://127.0.0.1:8000/api/tarefas/';

const tarefas = ref([]);
const loading = ref(true);

const buscarTarefas = async () => {
  loading.value = true;
  try {
    const response = await axios.get(API_URL);
    tarefas.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar tarefas:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(buscarTarefas);
</script>

<template>
  <div class="container">
    <header class="app-header">
      <h1>🚀 Gerenciador de Tarefas</h1>
      <p>Organize, priorize e conquiste seus objetivos.</p>
    </header>

    <main class="tasks-container">
      <div v-if="loading" class="feedback-message">Carregando tarefas... ⏳</div>
      <div v-else-if="tarefas.length === 0" class="feedback-message">
        🎉 Nenhuma tarefa na lista. Comece adicionando uma!
      </div>
      <ul v-else class="task-list">
        <TaskItem
          v-for="tarefa in tarefas"
          :key="tarefa.id"
          :tarefa="tarefa"
        />
      </ul>
    </main>
  </div>
</template>

<style>
/* Estilos globais (os mesmos do passo 1) */
body {
  background-color: #f4f7f9;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  margin: 0;
}
.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
}
.app-header {
  text-align: center;
  margin-bottom: 2.5rem;
}
.task-list { list-style: none; padding: 0; }
.feedback-message { text-align: center; padding: 3rem 1rem; color: #777; }
</style>