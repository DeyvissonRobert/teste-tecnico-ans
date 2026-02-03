<template>
  <div>
    <h1>Operadoras</h1>

    <!-- CAMPO DE BUSCA -->
    <input
      v-model="search"
      type="text"
      placeholder="Buscar por CNPJ ou Razão Social"
      style="margin-bottom: 16px; padding: 6px; width: 300px"
    />

    <!-- GRÁFICO -->
    <div style="max-width: 800px; margin-bottom: 40px;">
      <Bar v-if="chartData" :data="chartData" />
      <p v-else>Carregando gráfico...</p>
    </div>

    <!-- TABELA -->
    <table border="1" cellpadding="8">
      <thead>
        <tr>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>UF</th>
          <th>Modalidade</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="op in operadorasFiltradas" :key="op.CNPJ">
          <td>
            <router-link :to="`/operadoras/${op.CNPJ}`">
              {{ op.CNPJ }}
            </router-link>
          </td>
          <td>{{ op.RazaoSocial }}</td>
          <td>{{ op.UF || "-" }}</td>
          <td>{{ op.Modalidade || "-" }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import api from "../services/api";

/* Chart.js */
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

const operadoras = ref([]);
const search = ref("");
const chartData = ref(null);

/* 🔍 BUSCA NO CLIENTE */
const operadorasFiltradas = computed(() => {
  if (!search.value) return operadoras.value;

  const termo = search.value.toLowerCase();

  return operadoras.value.filter(op =>
    String(op.CNPJ).includes(termo) ||
    (op.RazaoSocial &&
      op.RazaoSocial.toLowerCase().includes(termo))
  );
});

onMounted(async () => {
  try {
    const response = await api.get("/operadoras");
    operadoras.value = response.data.data;

    gerarGrafico(operadoras.value);
  } catch (error) {
    console.error("Erro ao buscar operadoras:", error);
  }
});

/* 📊 GRÁFICO DE DESPESAS POR UF */
function gerarGrafico(dados) {
  const despesasPorUF = {};

  dados.forEach(item => {
    const uf = item.UF || "Não informado";
    const valor = Number(item.ValorDespesas) || 0;

    despesasPorUF[uf] = (despesasPorUF[uf] || 0) + valor;
  });

  chartData.value = {
    labels: Object.keys(despesasPorUF),
    datasets: [
      {
        label: "Despesas por UF",
        data: Object.values(despesasPorUF),
        // backgroundColor: "#9662C4",
        backgroundColor: "#FDBB2D",

      },
    ],
  };
}
</script>
