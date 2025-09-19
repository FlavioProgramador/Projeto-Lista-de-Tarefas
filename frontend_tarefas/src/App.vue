<script setup>
import { ref, onMounted, computed } from 'vue';
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
const filtroStatus = ref('TODOS');
const ordem = ref('data_termino_asc');
const toast = ref({ message: '', type: '', visible: false });
const modoEdicao = ref(false);
const tarefaParaEditar = ref(null);

const mostrarToast = (message, type = 'success') => {
  toast.value = { message, type, visible: true };
  setTimeout(() => { toast.value.visible = false; }, 3000);
};

const tarefasFiltradasEOrdenadas = computed(() => {
  let tarefasProcessadas = [...tarefas.value];
  if (filtroStatus.value !== 'TODOS') {
    tarefasProcessadas = tarefasProcessadas.filter(t => t.status === filtroStatus.value);
  }
  switch (ordem.value) {
    case 'data_termino_asc':
      tarefasProcessadas.sort((a, b) => new Date(a.data_termino) - new Date(b.data_termino));
      break;
    case 'data_termino_desc':
      tarefasProcessadas.sort((a, b) => new Date(b.data_termino) - new Date(a.data_termino));
      break;
    case 'prioridade':
      const prioridadeValor = { 'ALTA': 3, 'MEDIA': 2, 'BAIXA': 1 };
      tarefasProcessadas.sort((a, b) => prioridadeValor[b.prioridade] - prioridadeValor[a.prioridade]);
      break;
  }
  return tarefasProcessadas;
});

const tarefasConcluidas = computed(() => {
  return tarefas.value.filter(t => t.status === 'FINALIZADA').length;
});

const iniciarEdicao = (tarefa) => {
  modoEdicao.value = true;
  tarefaParaEditar.value = { ...tarefa };
  novaTarefa.value = { ...tarefa };
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const cancelarEdicao = () => {
  modoEdicao.value = false;
  tarefaParaEditar.value = null;
  novaTarefa.value = getTarefaInicial();
};

const buscarTarefas = async () => {
  loading.value = true;
  try {
    const response = await axios.get(API_URL);
    tarefas.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar tarefas:', error);
    mostrarToast('Não foi possível carregar as tarefas.', 'error');
  } finally {
    loading.value = false;
  }
};

const handleSubmit = () => {
  if (modoEdicao.value) {
    salvarAlteracoes();
  } else {
    adicionarTarefa();
  }
};

const adicionarTarefa = async () => {
  if (!novaTarefa.value.titulo || !novaTarefa.value.data_termino) {
    mostrarToast('Preencha os campos obrigatórios.', 'error');
    return;
  }
  isSubmitting.value = true;
  const tarefaTemporaria = { ...novaTarefa.value, id: Date.now() };
  tarefas.value.unshift(tarefaTemporaria);
  try {
    const response = await axios.post(API_URL, novaTarefa.value);
    const index = tarefas.value.findIndex(t => t.id === tarefaTemporaria.id);
    if (index !== -1) tarefas.value[index] = response.data;
    novaTarefa.value = getTarefaInicial();
    mostrarToast('Tarefa adicionada com sucesso!');
  } catch (error) {
    console.error('Erro ao adicionar tarefa:', error);
    mostrarToast('Erro ao salvar a tarefa.', 'error');
    tarefas.value = tarefas.value.filter(t => t.id !== tarefaTemporaria.id);
  } finally {
    isSubmitting.value = false;
  }
};

const salvarAlteracoes = async () => {
  if (!tarefaParaEditar.value) return;
  isSubmitting.value = true;
  const id = tarefaParaEditar.value.id;
  const index = tarefas.value.findIndex(t => t.id === id);
  if (index === -1) {
    isSubmitting.value = false;
    return;
  }
  const tarefaOriginal = { ...tarefas.value[index] };
  tarefas.value[index] = { ...tarefaOriginal, ...novaTarefa.value };
  try {
    const response = await axios.patch(`${API_URL}${id}/`, novaTarefa.value);
    tarefas.value[index] = { ...tarefas.value[index], ...response.data };
    mostrarToast('Tarefa atualizada com sucesso!');
    cancelarEdicao();
  } catch (error) {
    console.error('Erro ao atualizar tarefa:', error);
    mostrarToast('Erro ao salvar. Alterações desfeitas.', 'error');
    tarefas.value[index] = tarefaOriginal;
  } finally {
    isSubmitting.value = false;
  }
};

const handleTaskDeleted = async (id) => {
  const index = tarefas.value.findIndex(t => t.id === id);
  if (index === -1) return;
  const tarefaRemovida = tarefas.value[index];
  tarefas.value.splice(index, 1);
  try {
    await axios.delete(`${API_URL}${id}/`);
    mostrarToast('Tarefa excluída.');
  } catch (error) {
    console.error('Erro ao excluir tarefa:', error);
    mostrarToast('Erro ao excluir. A tarefa foi restaurada.', 'error');
    tarefas.value.splice(index, 0, tarefaRemovida);
  }
};

const handleStatusUpdated = async (tarefaAtualizada) => {
  const index = tarefas.value.findIndex(t => t.id === tarefaAtualizada.id);
  if (index === -1) return;
  const statusAntigo = tarefas.value[index].status;
  tarefas.value[index] = tarefaAtualizada;
  try {
    await axios.patch(`${API_URL}${tarefaAtualizada.id}/`, { status: tarefaAtualizada.status });
    mostrarToast(`Status alterado para "${tarefaAtualizada.status}".`);
  } catch (error) {
    console.error('Erro ao atualizar status:', error);
    mostrarToast('Erro ao atualizar status. Revertendo.', 'error');
    tarefas.value[index].status = statusAntigo;
  }
};

onMounted(buscarTarefas);
</script>

<template>
  <div v-if="toast.visible" class="toast" :class="toast.type">{{ toast.message }}</div>

  <div class="container">
    <header class="app-header">
      <h1>🚀 Gerenciador de Tarefas</h1>
      <p>Organize, priorize e conquiste seus objetivos.</p>
    </header>

    <div class="form-container card">
      <h3>{{ modoEdicao ? '✍️ Editando Tarefa' : '➕ Adicionar Nova Tarefa' }}</h3>
      <form @submit.prevent="handleSubmit" class="task-form">
        <input class="input-titulo" type="text" v-model="novaTarefa.titulo" placeholder="O que precisa ser feito? *" required />
        <textarea class="input-descricao" v-model="novaTarefa.descricao" placeholder="Adicione uma descrição..."></textarea>
        <div class="form-row">
          <div class="form-group">
            <label for="data-inicio">Início</label>
            <input id="data-inicio" type="date" v-model="novaTarefa.data_inicio" required title="Data de Início" />
          </div>
          <div class="form-group">
            <label for="data-termino">Término</label>
            <input id="data-termino" type="date" v-model="novaTarefa.data_termino" required title="Data de Término" />
          </div>
          <div class="form-group">
            <label for="prioridade">Prioridade</label>
            <select id="prioridade" v-model="novaTarefa.prioridade" title="Prioridade">
              <option value="BAIXA">Baixa</option>
              <option value="MEDIA">Média</option>
              <option value="ALTA">Alta</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn-cancel" v-if="modoEdicao" @click="cancelarEdicao">
            Cancelar
          </button>
          <button type="submit" class="btn-submit" :disabled="isSubmitting">
            <span v-if="isSubmitting">Salvando...</span>
            <span v-else>{{ modoEdicao ? 'Salvar Alterações' : '+ Adicionar' }}</span>
          </button>
        </div>
      </form>
    </div>
    
    <main class="tasks-container">
      <div class="list-controls">
        <div class="filters">
          <span>Filtrar por:</span>
          <button :class="{ active: filtroStatus === 'TODOS' }" @click="filtroStatus = 'TODOS'">Todos</button>
          <button :class="{ active: filtroStatus === 'PENDENTE' }" @click="filtroStatus = 'PENDENTE'">Pendente</button>
          <button :class="{ active: filtroStatus === 'ANDAMENTO' }" @click="filtroStatus = 'ANDAMENTO'">Andamento</button>
          <button :class="{ active: filtroStatus === 'FINALIZADA' }" @click="filtroStatus = 'FINALIZADA'">Finalizada</button>
        </div>
        <div class="sort">
          <label for="sort-select">Ordenar por:</label>
          <select id="sort-select" v-model="ordem">
            <option value="data_termino_asc">Prazo (mais próximo)</option>
            <option value="data_termino_desc">Prazo (mais distante)</option>
            <option value="prioridade">Prioridade</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="feedback-message">Carregando tarefas... ⏳</div>
      <div v-else-if="tarefasFiltradasEOrdenadas.length === 0" class="feedback-message">
        <div v-if="tarefas.length === 0">🎉 Nenhuma tarefa na lista. Comece adicionando uma!</div>
        <div v-else>🔍 Nenhuma tarefa encontrada com este filtro.</div>
      </div>
      <ul v-else class="task-list">
        <transition-group name="fade">
          <TaskItem
            v-for="tarefa in tarefasFiltradasEOrdenadas"
            :key="tarefa.id"
            :tarefa="tarefa"
            @statusUpdated="handleStatusUpdated"
            @taskDeleted="handleTaskDeleted"
            @editTask="iniciarEdicao"
          />
        </transition-group>
      </ul>
      <footer class="app-footer">
        <span>Total de tarefas: {{ tarefas.length }}</span> | <span>Concluídas: {{ tarefasConcluidas }}</span>
      </footer>
    </main>
  </div>
</template>

<style>
:root {
  --color-primary: #4a90e2;
  --color-primary-dark: #357ABD;
  --color-background: #f4f7f9;
  --color-surface: #ffffff;
  --color-text-primary: #2c3e50;
  --color-text-secondary: #5a6e81;
  --color-border: #e0e6ed;
  --color-status-pendente: #f39c12;
  --color-status-andamento: #3498db;
  --color-status-finalizada: #2ecc71;
  --color-priority-baixa: #1abc9c;
  --color-priority-media: #f1c40f;
  --color-priority-alta: #e74c3c;
  --shadow-md: 0 4px 10px rgba(0,0,0,0.08);
}
body {
  background-color: var(--color-background);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--color-text-primary);
  margin: 0;
}
.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
}
.card {
  background: var(--color-surface);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
}
.app-header { text-align: center; margin-bottom: 2.5rem; }
.app-header h1 { margin: 0; color: var(--color-text-primary); font-size: 2.5rem; }
.app-header p { color: var(--color-text-secondary); }
.form-container { padding: 2rem; margin-bottom: 2.5rem; }
.task-form { display: flex; flex-direction: column; gap: 1rem; }
.task-form input, .task-form textarea, .task-form select {
  padding: 0.8rem 1rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  font-size: 1rem;
  transition: all 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}
.task-form input:focus, .task-form textarea:focus, .task-form select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}
.task-form textarea { resize: vertical; min-height: 60px; }
.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  align-items: end;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  padding-left: 0.25rem;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
.form-actions button {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-submit { background-color: var(--color-primary); color: white; }
.btn-submit:hover:not(:disabled) { background-color: var(--color-primary-dark); }
.btn-submit:disabled { background-color: #bdc3c7; cursor: not-allowed; }
.btn-cancel { background-color: #f1f3f5; color: var(--color-text-secondary); }
.btn-cancel:hover { background-color: #e9ecef; }
.list-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 0 0.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.filters { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
.filters span { font-size: 0.9rem; color: var(--color-text-secondary); margin-right: 0.5rem; }
.filters button {
  background: none;
  border: 1px solid var(--color-border);
  padding: 0.4rem 0.8rem;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.filters button.active { background-color: var(--color-primary); color: white; border-color: var(--color-primary); }
.filters button:hover:not(.active) { background-color: #e8e8e8; }
.sort { display: flex; gap: 0.5rem; align-items: center; }
.sort label { font-size: 0.9rem; color: var(--color-text-secondary); }
.sort select { border-radius: 6px; padding: 0.4rem 0.6rem; border: 1px solid var(--color-border); }
.feedback-message { text-align: center; padding: 3rem 1rem; color: #777; }
.task-list { list-style: none; padding: 0; }
.fade-enter-active, .fade-leave-active { transition: all 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(20px); }
.app-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  font-size: 0.9rem;
}
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 1rem 1.5rem;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  animation: slide-in 0.3s ease;
}
.toast.success { background-color: var(--color-status-finalizada); }
.toast.error { background-color: var(--color-priority-alta); }
@keyframes slide-in { from { bottom: -50px; opacity: 0; } to { bottom: 20px; opacity: 1; } }
</style>