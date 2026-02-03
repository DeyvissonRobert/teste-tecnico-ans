<template>
  <div class="container">
    <h1>Detalhes da Operadora</h1>

    <p><strong>CNPJ:</strong> {{ cnpj }}</p>

    <button class="btn-voltar" @click="voltar">⬅ Voltar</button>

    <h2>Histórico de Despesas</h2>

    <!-- Loading -->
    <p v-if="loading">Carregando despesas...</p>

    <!-- Tabela -->
    <table v-if="!loading && despesasPaginadas.length" border="1" cellpadding="8">
      <thead>
        <tr>
          <th>Ano</th>
          <th>Trimestre</th>
          <th>Valor</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(d, index) in despesasPaginadas" :key="index">
          <td>{{ d.Ano }}</td>
          <td>{{ d.Trimestre }}</td>
          <td>{{ formatarValor(d.ValorDespesas) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="!loading && despesas.length === 0">
      Nenhuma despesa encontrada para esta operadora.
    </p>

    <!-- Paginação -->
      <button @click="irParaPagina(paginaAtual - 1)" :disabled="paginaAtual === 1">
        ‹
      </button>

      <button
        v-for="pagina in paginasVisiveis"
        :key="pagina"
        :disabled="pagina === '...'"
        @click="pagina !== '...' && irParaPagina(pagina)"
        :class="{ ativo: pagina === paginaAtual, dots: pagina === '...' }"
      >
        {{ pagina }}
      </button>

      <button
        @click="irParaPagina(paginaAtual + 1)"
        :disabled="paginaAtual === totalPaginas"
      >
        ›
      </button>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const cnpj = route.params.cnpj;

const despesas = ref([]);
const loading = ref(true);

// Paginação
const paginaAtual = ref(1);
const itensPorPagina = 20;
const maxPaginasVisiveis = 9;

const totalPaginas = computed(() =>
  Math.ceil(despesas.value.length / itensPorPagina)
);

const despesasPaginadas = computed(() => {
  const inicio = (paginaAtual.value - 1) * itensPorPagina;
  const fim = inicio + itensPorPagina;
  return despesas.value.slice(inicio, fim);
});

const paginasVisiveis = computed(() => {
  const paginas = [];
  const total = totalPaginas.value;
  const atual = paginaAtual.value;

  // Sempre começa do 1
  paginas.push(1);

  // Janela intermediária
  let inicio = Math.max(2, atual - 2);
  let fim = Math.min(total - 1, atual + 2);

  if (inicio > 2) {
    paginas.push("...");
  }

  for (let i = inicio; i <= fim; i++) {
    paginas.push(i);
  }

  if (fim < total - 1) {
    paginas.push("...");
  }

  if (total > 1) {
    paginas.push(total);
  }

  return paginas;
});



function irParaPagina(pagina) {
  if (pagina >= 1 && pagina <= totalPaginas.value) {
    paginaAtual.value = pagina;
  }
}

function voltar() {
  router.back();
}

function formatarValor(valor) {
  return Number(valor).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

onMounted(async () => {
  try {
    const response = await api.get(`/operadoras/${cnpj}/despesas`);
    despesas.value = response.data.despesas || [];
  } catch (error) {
    console.error("Erro ao buscar despesas:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.container {
  text-align: center;
}

.btn-voltar {
  margin: 10px 0 20px;
  background: none;
  border: none;
  color: #4f7cff;
  cursor: pointer;
  font-size: 16px;
}

table {
  margin: 0 auto;
  border-collapse: collapse;
}

th,
td {
  padding: 8px 12px;
}

.pagination {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 6px;
  flex-wrap: wrap;
}

.pagination button {
  padding: 6px 10px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.pagination button.dots {
  cursor: default;
  background: transparent;
}

.pagination button.ativo {
  background-color: #4f7cff;
  color: white;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
