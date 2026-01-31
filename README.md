# Teste Técnico – ANS

## Visão Geral
Este projeto foi desenvolvido como parte de um teste técnico, com o objetivo de coletar, processar e organizar dados públicos da ANS (Agência Nacional de Saúde Suplementar).

A solução contempla desde a obtenção dos arquivos brutos até a consolidação dos dados em um formato estruturado, priorizando simplicidade, clareza e decisões técnicas bem justificadas.

## Estrutura do Projeto

- `01_api_ans/`  
  Contém os scripts responsáveis pela coleta, processamento e análise dos dados da ANS.

- `data/raw/`  
  Arquivos originais baixados da ANS (formato ZIP).

- `data/processed/`  
  Dados processados e consolidados ao longo do pipeline.

- `data/processed/analises/`  
  Arquivos CSV finais gerados a partir das análises realizadas.

- `venv/`  
  Ambiente virtual Python utilizado no desenvolvimento do projeto.

## 👣 Etapas do Desenvolvimento

### 1.1 Coleta dos Dados
Os dados foram obtidos a partir das Demonstrações Contábeis disponibilizadas pela ANS.

Inicialmente considerei a listagem automática dos arquivos via FTP, porém identifiquei instabilidades no servidor (erros de listagem e sensibilidade a maiúsculas/minúsculas).

Para garantir uma solução simples e estável, optei pelo download direto dos arquivos a partir de seus nomes conhecidos, seguindo o padrão oficial da ANS (ex: `4T2023.zip`).  
Os arquivos são armazenados no diretório `data/raw`.

---

### 1.2 Transformação Inicial dos Dados
Após o download, os arquivos ZIP foram extraídos e convertidos para o formato CSV.

Optei por trabalhar diretamente com arquivos CSV ao longo do pipeline, priorizando simplicidade, legibilidade e compatibilidade com as etapas seguintes, considerando o prazo e o escopo do desafio.

---

### 1.3 Consolidação e Análise de Inconsistências
Os dados dos trimestres analisados foram consolidados em um único arquivo (`consolidado_despesas.csv`), contendo as colunas exigidas pelo teste:
- CNPJ  
- RazaoSocial  
- Trimestre  
- Ano  
- ValorDespesas  

Durante a consolidação, tratei as seguintes inconsistências:
- Valores zerados ou negativos foram descartados
- Datas em formatos inconsistentes foram convertidas com tolerância a erro
- O campo `REG_ANS` foi utilizado como identificador temporário de operadora, o que foi documentado como uma limitação dos dados disponíveis

---

### 2.1 Limpeza e Padronização dos Dados
Os valores monetários, originalmente representados como texto com separador decimal em vírgula, foram limpos e convertidos explicitamente para formato numérico.

Também realizei padronizações de tipos de dados e remoção de registros inválidos, garantindo maior consistência para as análises posteriores.

---

### 2.2 Enriquecimento dos Dados com Cadastro de Operadoras
Os dados consolidados de despesas foram enriquecidos com informações cadastrais das operadoras ativas da ANS.

Realizei um join utilizando o CNPJ como chave, adicionando as colunas RegistroANS, Modalidade e UF. O processo foi documentado considerando casos de ausência ou duplicidade de CNPJ no cadastro oficial.

---

### 2.3 Agregação de Despesas por Operadora e UF
Os dados enriquecidos foram agregados por RazaoSocial e UF, conforme solicitado no teste.

Para cada grupo, foram calculados:
- Total de despesas
- Média de despesas por trimestre
- Desvio padrão das despesas, com o objetivo de identificar variações significativas nos valores

O resultado foi ordenado pelo total de despesas (do maior para o menor) e salvo no arquivo `despesas_agregadas.csv`.

Essa etapa reduz significativamente o volume de dados, transformando registros individuais em informações consolidadas e mais adequadas para análise.

---

### 3. Escolha do banco de dados
Optei por usar PostgreSQL em vez de MySQL porque ele é mais flexível para análises, lida melhor com consultas mais complexas e tem suporte mais completo a funções analíticas.

Para este teste, onde o foco está em análise de dados e queries mais elaboradas, o PostgreSQL se mostrou mais adequado e simples de trabalhar.

---

### 3. Banco de Dados e Análise SQL
Criei scripts SQL compatíveis com PostgreSQL para estruturar o banco de dados, importar os arquivos CSV gerados nas etapas anteriores e responder às consultas analíticas solicitadas no teste.

Os scripts incluem:
- Criação das tabelas com tipos de dados e índices apropriados
- Exemplos de importação dos dados a partir dos arquivos CSV
- Queries analíticas para análise de crescimento de despesas, distribuição por UF e comparação com médias

## 🛠️ Trade-offs Técnicos

### 1.2 Download direto dos arquivos em vez de listagem automática
A listagem dinâmica via FTP foi descartada devido a instabilidades encontradas durante os testes.

O download direto pelos nomes conhecidos reduz a complexidade da solução e aumenta a confiabilidade, ao custo de exigir atualização manual caso o padrão dos arquivos seja alterado.

---

### 2.1 Leitura de dados com tolerância a inconsistências
Durante a leitura dos arquivos CSV, identifiquei linhas com formato inconsistente.

Em vez de interromper o processamento, optei por permitir o descarte dessas linhas, priorizando a continuidade do pipeline e a robustez da solução, mesmo com a perda de alguns registros problemáticos.

### 2.1 Conversão explícita de valores monetários
Escolhi realizar a conversão manual dos valores monetários para formato numérico, em vez de depender de configurações de locale.

Essa decisão torna o processamento mais previsível, independente do ambiente de execução e mais seguro para análises e agregações futuras.

---

### 2.2 Estratégia de join e tratamento de inconsistências no cadastro de operadoras
Durante o enriquecimento dos dados, foi necessário realizar um join entre o arquivo consolidado de despesas e o cadastro de operadoras ativas da ANS, utilizando o CNPJ como chave.

Optei por utilizar um left join, garantindo que todos os registros de despesas fossem preservados, mesmo quando não houvesse correspondência no cadastro de operadoras.

Para tratar inconsistências:
- CNPJs sem correspondência no cadastro foram mantidos, com campos de cadastro nulos
- CNPJs duplicados no cadastro foram resolvidos mantendo apenas um registro por CNPJ

Essa abordagem prioriza a integridade dos dados financeiros e evita a perda de informações relevantes, ao custo de manter registros parcialmente enriquecidos, o que considerei aceitável para fins analíticos.

---

### 2.3 Estratégia de agregação e ordenação dos dados
Para a etapa de agregação, optei por realizar os cálculos diretamente utilizando operações de groupby no Pandas, considerando o volume atual dos dados e o escopo do desafio.

Essa abordagem simplifica a implementação, mantém o código legível e apresenta boa performance para o tamanho do dataset utilizado.

A ordenação foi realizada em memória, priorizando clareza e rapidez de desenvolvimento. Em cenários com volumes significativamente maiores, estratégias como processamento incremental ou uso direto de banco de dados seriam consideradas.

---

### 3.2 Normalização e escolha de tipos de dados
Optei por manter tabelas separadas para despesas, operadoras e dados agregados, em vez de utilizar uma única tabela desnormalizada.

Essa abordagem reduz redundância, deixa o modelo mais organizado e facilita consultas analíticas, mesmo aumentando um pouco a complexidade das queries.

Para valores monetários, escolhi o tipo DECIMAL, priorizando precisão nos cálculos financeiros em vez de performance extrema.

---

### 3.4 Estratégia das queries analíticas
Optei por construir as queries utilizando CTEs (Common Table Expressions), pois deixam o código mais legível e fácil de entender.

Mesmo existindo formas mais curtas de escrever algumas consultas, priorizei clareza e manutenibilidade, pensando em quem irá avaliar ou dar manutenção no código.

## Como Executar o Projeto

1. Clone o repositório e acesse o diretório do projeto.
   ```bash
   git clone <url-do-repositorio>
   cd Teste_DeyvissonRobert 
   ```
2. Crie e ative um ambiente virtual Python.
    ```bash
    python -m venv venv
   ```
     Windows
       ```bash
        venv\Scripts\activate
       ```
    Linux / Mac
       ```bash
        source venv/bin/activate
       ```
3. Instale as dependências necessárias.
    ```bash
    pip install pandas requests
   ```
4. Execute o script de download dos dados.
   ```bash
   python 01_api_ans/download_dados.py
   ```
5. Execute o script de processamento e consolidação.
   ```bash
   python 01_api_ans/processar_despesas.py
   ```
6. Execute o script de análise dos dados.
   ```bash
   python 01_api_ans/analise_despesas.py
   ```
   
## Considerações Finais

Este projeto foi desenvolvido com foco em simplicidade, reprodutibilidade e clareza técnica.

Ao longo do desafio, priorizei decisões que garantissem estabilidade do pipeline e facilidade de entendimento, mesmo diante de limitações e inconsistências nos dados públicos disponibilizados.

A solução final entrega um fluxo completo de coleta, processamento, consolidação e análise, além de documentação clara sobre as decisões técnicas e trade-offs adotados.
