

## Coleta dos Dados

# 01 
Durante os testes identifiquei que o FTP da ANS apresenta algumas limitações…
Os dados foram obtidos a partir das Demonstrações Contábeis disponibilizadas pela ANS.

Inicialmente, considerei listar dinamicamente os arquivos disponíveis no FTP, porém durante os testes identifiquei limitações no acesso via HTTP (erros de listagem, sensibilidade a maiúsculas/minúsculas e respostas inconsistentes do servidor).  

Para evitar instabilidades e garantir uma solução simples e reprodutível, optei por realizar o download direto dos arquivos a partir de seus nomes conhecidos, seguindo o padrão oficial adotado pela ANS (ex: `4T2023.zip`).

Foram utilizados os últimos trimestres completos disponíveis (2T, 3T e 4T de 2023). Os arquivos são baixados automaticamente pelo script `download_dados.py` e armazenados no diretório `data/raw`.

