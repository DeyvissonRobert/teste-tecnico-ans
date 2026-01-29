

## Coleta dos Dados

### Decisão técnica

Durante o desenvolvimento, avaliei duas abordagens para obter os arquivos da ANS:

- Listar dinamicamente os diretórios e arquivos disponíveis no FTP
- Realizar o download direto dos arquivos a partir de seus nomes conhecidos

Inicialmente tentei a listagem dinâmica, porém durante os testes identifiquei limitações no acesso via HTTP, como erros 404 intermitentes, sensibilidade a maiúsculas/minúsculas nos caminhos e respostas inconsistentes do servidor.

Diante disso, optei pela abordagem de download direto utilizando o padrão oficial de nomenclatura adotado pela ANS (ex: `4T2023.zip`).

**Prós da abordagem escolhida:**
- Maior estabilidade na execução
- Código mais simples e previsível
- Facilidade de reprodução do processo

**Contras considerados:**
- Menor flexibilidade para novos períodos
- Necessidade de ajuste manual caso o padrão de nomes mude

Os dados utilizados correspondem aos últimos trimestres completos disponíveis (2T, 3T e 4T de 2023).  
Os arquivos são baixados automaticamente pelo script `download_dados.py` e armazenados no diretório `data/raw`.


