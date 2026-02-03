import { createRouter, createWebHistory } from "vue-router";
import ListaOperadoras from "../pages/ListaOperadoras.vue";
import DetalheOperadora from "../pages/DetalheOperadora.vue";

const routes = [
  {
    path: "/",
    name: "lista-operadoras",
    component: ListaOperadoras,
  },
  {
    path: "/operadoras/:cnpj",
    name: "detalhe-operadora",
    component: DetalheOperadora,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
