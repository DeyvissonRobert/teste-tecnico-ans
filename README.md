# Teste Técnico – ANS

## Visão Geral
Para que eu possa explicar o desafio e o que fiz

## Estrutura do Projeto


## Etapas do Desenvolvimento

### 1. Coleta dos Dados
Os dados foram obtidos a partir das Demonstrações Contábeis disponibilizadas pela ANS.
Inicialmente tentei realizar a listagem automática dos arquivos via FTP, porém encontrei instabilidades no acesso (erros de listagem e sensibilidade a maiúsculas/minúsculas).

Para garantir uma solução simples e estável, optei por realizar o download direto dos arquivos a partir de seus nomes conhecidos, seguindo o padrão oficial da ANS (ex: `4T2023.zip`).  
Os arquivos baixados são armazenados no diretório `data/raw`.

### 2. Processamento e Consolidação
Após o download, os arquivos foram extraídos e convertidos para CSV.
Em seguida, os dados dos três trimestres selecionados (2T, 3T e 4T de 2023) foram consolidados em um único arquivo (`despesas_consolidadas.csv`), facilitando a análise posterior.

Durante essa etapa, foi necessário tratar inconsistências no formato dos dados e padronizar os tipos das colunas.


## Trade-offs Técnicos

### 1. Download direto dos arquivos em vez de listagem automática

Inicialmente considerei listar dinamicamente os arquivos disponíveis no FTP da ANS.
No entanto, durante os testes, encontrei instabilidades no acesso e respostas inconsistentes do servidor.

Optei por realizar o download direto dos arquivos a partir de seus nomes conhecidos.
Essa abordagem reduz a complexidade e garante maior estabilidade, embora exija atualização manual caso o padrão de nomes seja alterado.

### 2. Leitura dos arquivos com tolerância a linhas inconsistentes

Durante a leitura do arquivo consolidado, identifiquei linhas com quantidade de colunas diferente do padrão esperado, o que causava erros no Pandas.

Avaliei alternativas mais complexas, mas optei por manter o parser padrão e permitir o descarte de linhas inválidas.
Essa decisão prioriza a continuidade do processamento e a robustez do pipeline, mesmo com a perda de alguns registros inconsistentes.

### 3. Conversão explícita dos valores monetários

Os valores monetários estavam representados como texto, utilizando vírgula como separador decimal.
Avaliei utilizar configurações de locale, porém optei por realizar a limpeza e conversão manual dos valores.

Essa abordagem torna o processamento mais previsível e independente do ambiente, facilitando análises e agregações posteriores.


## Como Executar o Projeto


## Considerações Finais
