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

## Etapas do Desenvolvimento

### 1.1 Coleta dos Dados
Os dados foram obtidos a partir das Demonstrações Contábeis disponibilizadas pela ANS.

Os arquivos correspondentes aos trimestres analisados foram baixados e armazenados localmente no diretório `data/raw`, mantendo os arquivos originais conforme disponibilizados pela fonte oficial.

---

### 1.3 Consolidação e Validação dos Dados
Após o processamento inicial, os dados dos trimestres selecionados foram consolidados em um único arquivo CSV (`consolidado_despesas.csv`).

Durante essa etapa:
- Foi extraído o ano a partir da coluna de data.
- Os valores monetários foram convertidos para formato numérico.
- Registros com valores zerados ou negativos foram removidos.
- Campos necessários para análise (CNPJ, Razão Social, Trimestre, Ano e Valor de Despesas) foram padronizados.

Como os dados contábeis não possuem CNPJ e Razão Social reais, o campo `REG_ANS` foi utilizado como identificador da operadora, e a coluna `DESCRICAO` como identificação textual, decisão documentada para garantir transparência.

---

### 2. Processamento e Análises Exploratórias
Com os dados consolidados, foram realizadas análises exploratórias simples para facilitar a compreensão das despesas, incluindo:
- Totalização por trimestre
- Totalização por conta contábil
- Totalização por descrição

Os resultados dessas análises foram salvos em arquivos CSV no diretório `data/processed/analises`, permitindo fácil visualização e reutilização dos dados.


## Trade-offs Técnicos

### 1.2 Download direto dos arquivos em vez de listagem automática 

Inicialmente foi considerada a listagem automática dos arquivos via FTP da ANS.  
Durante os testes, foram identificadas instabilidades no serviço, como falhas de listagem e sensibilidade a variações de nomenclatura.

Como trade-off, foi adotado o download direto dos arquivos a partir de seus nomes conhecidos, seguindo o padrão oficial da ANS (ex: `2T2023.zip`, `3T2023.zip`, `4T2023.zip`).

Essa decisão reduz a complexidade da solução e aumenta a estabilidade do pipeline, ao custo de exigir atualização manual caso o padrão de nomes seja alterado no futuro.

---

### 2.3 Geração de arquivos agregados para análise

Para a etapa de análise, foi avaliada a possibilidade de realizar todas as agregações diretamente sobre o arquivo consolidado sempre que necessário.

Como trade-off, optou-se por gerar arquivos CSV agregados separados para cada análise realizada.  
Essa abordagem aumenta o número de arquivos gerados, porém melhora a organização do projeto, facilita a reutilização dos resultados e torna a validação das análises mais clara para avaliadores e usuários finais.

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
