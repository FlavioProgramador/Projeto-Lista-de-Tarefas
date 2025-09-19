<script setup>
import { computed } from 'vue';

const props = defineProps({
  tarefa: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['statusUpdated', 'taskDeleted', 'editTask']);
const handleStatusChange = (event) => {
  const updatedTask = { ...props.tarefa, status: event.target.value };
  emit('statusUpdated', updatedTask);
};

const handleDelete = () => {
  if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
    emit('taskDeleted', props.tarefa.id);
  }
};

const formatarData = (dataString) => {
  if (!dataString) return 'N/A';
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dataString + 'T00:00:00').toLocaleDateString('pt-BR', options);
};

const dataInicioFormatada = computed(() => formatarData(props.tarefa.data_inicio));
const dataTerminoFormatada = computed(() => formatarData(props.tarefa.data_termino));
</script>

<template>
  <li class="task-card" :class="tarefa.status.toLowerCase()">
    <div class="task-card-header">
      <h3 class="task-title">{{ tarefa.titulo }}</h3>
      <span class="task-priority" :class="tarefa.prioridade.toLowerCase()">{{ tarefa.prioridade }}</span>
    </div>

    <p v-if="tarefa.descricao" class="task-description">{{ tarefa.descricao }}</p>

    <div class="task-card-footer">
      <div class="task-dates">
        <span>🗓️ Início: {{ dataInicioFormatada }}</span>
        <span>🏁 Término: {{ dataTerminoFormatada }}</span>
      </div>

      <div class="task-controls">
        <select :value="tarefa.status" @change="handleStatusChange" class="status-select" title="Alterar status">
          <option value="PENDENTE">Pendente</option>
          <option value="ANDAMENTO">Em Andamento</option>
          <option value="FINALIZADA">Finalizada</option>
        </select>

        <button @click="emit('editTask', tarefa)" class="btn-icon btn-edit" title="Editar tarefa">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        </button>

        <button @click="handleDelete" class="btn-icon btn-delete" title="Excluir tarefa">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
        </button>
      </div>
    </div>
  </li>
</template>

<style scoped>
.task-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border-left: 6px solid;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.task-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}
.task-card.pendente { border-left-color: var(--color-status-pendente); }
.task-card.andamento { border-left-color: var(--color-status-andamento); }
.task-card.finalizada {
  border-left-color: var(--color-status-finalizada);
  opacity: 0.7;
}
.task-card.finalizada .task-title {
  text-decoration: line-through;
  color: #888;
}
.task-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}
.task-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
}
.task-priority {
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  text-transform: uppercase;
  flex-shrink: 0;
}
.task-priority.baixa { background-color: var(--color-priority-baixa); }
.task-priority.media { background-color: var(--color-priority-media); color: #333; }
.task-priority.alta { background-color: var(--color-priority-alta); }
.task-description {
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin: 0;
}
.task-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f0f0f0;
}
.task-dates {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #777;
  align-items: center;
}
.task-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.status-select {
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  cursor: pointer;
}
.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.4rem;
  line-height: 1;
  border-radius: 50%;
  color: #999;
  transition: all 0.2s ease;
}
.btn-edit:hover {
  background-color: #eaf3fe;
  color: var(--color-primary);
}
.btn-delete:hover {
  background-color: #fce8e8;
  color: var(--color-priority-alta);
}
</style>