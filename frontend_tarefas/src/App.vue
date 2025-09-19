<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import TaskItem from './components/TaskItem.vue';

const API_URL = 'http://127.0.0.1:8000/api/tarefas/';

const getTarefaInicial = () => ({
  titulo: '',
  descricao: '',
  data_inicio: new Date().toISOString().split('T')[0],
  data_termino: '',
  prioridade: 'MEDIA',
  status: 'PENDENTE'
});

const tarefas = ref([]);
const novaTarefa = ref(getTarefaInicial());
const loading = ref(true);
const isSubmitting = ref(false);

const buscarTarefas = async () => { /* ...código do passo anterior... */ };

const adicionarTarefa = async () => {
  if (!novaTarefa.value.titulo || !novaTarefa.value.data_termino) {
    alert('Preencha os campos obrigatórios.');
    return;
  }
  isSubmitting.value = true;
  // Atualização Otimista
  const tarefaTemporaria = { ...novaTarefa.value, id: Date.now() };
  tarefas.value.unshift(tarefaTemporaria);

  try {
    const response = await axios.post(API_URL, novaTarefa.value);
    // Substitui a tarefa temporária pela real vinda da API
    const index = tarefas.value.findIndex(t => t.id === tarefaTemporaria.id);
    if (index !== -1) tarefas.value[index] = response.data;
    novaTarefa.value = getTarefaInicial();
  } catch (error) {
    console.error('Erro ao adicionar tarefa:', error);
    alert('Erro ao salvar a tarefa.');
    // Reverte a atualização otimista em caso de erro
    tarefas.value = tarefas.value.filter(t => t.id !== tarefaTemporaria.id);
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(buscarTarefas);
</script>

<template>
  <div class="container">
    <header class="app-header">
      </header>

    <div class="form-container card">
      <h3>➕ Adicionar Nova Tarefa</h3>
      <form @submit.prevent="adicionarTarefa" class="task-form">
        <input type="text" v-model="novaTarefa.titulo" placeholder="O que precisa ser feito? *" required />
        <textarea v-model="novaTarefa.descricao" placeholder="Adicione uma descrição..."></textarea>
        <div class="form-row">
          <div class="form-group">
            <label for="data-termino">Término</label>
            <input id="data-termino" type="date" v-model="novaTarefa.data_termino" required />
          </div>
          <div class="form-group">
            <label for="prioridade">Prioridade</label>
            <select id="prioridade" v-model="novaTarefa.prioridade">
              <option value="BAIXA">Baixa</option>
              <option value="MEDIA">Média</option>
              <option value="ALTA">Alta</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="isSubmitting">
            <span v-if="isSubmitting">Salvando...</span>
            <span v-else>+ Adicionar</span>
          </button>
        </div>
      </form>
    </div>

    <main class="tasks-container">
      </main>
  </div>
</template>

<style>
/* ...estilos globais anteriores... */
.card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
.form-container { padding: 2rem; margin-bottom: 2.5rem; }
.task-form { display: flex; flex-direction: column; gap: 1rem; }
.task-form input, .task-form textarea, .task-form select {
  padding: 0.8rem 1rem;
  border-radius: 8px;
  border: 1px solid #e0e6ed;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
}
.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-size: 0.85rem; font-weight: 500; }
.form-actions { display: flex; justify-content: flex-end; }
.btn-submit {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  background-color: #4a90e2;
  color: white;
}
.btn-submit:disabled { background-color: #bdc3c7; cursor: not-allowed; }
</style>