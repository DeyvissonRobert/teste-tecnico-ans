-- ============================
-- 3.3 Importação dos dados CSV
-- ============================

-- 1) Importar dados consolidados de despesas (1.3)
COPY despesas_consolidadas (
    cnpj,
    razao_social,
    trimestre,
    ano,
    valor_despesas
)
FROM '/caminho/para/consolidado_despesas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';


-- 2) Importar dados consolidados enriquecidos (2.2)
COPY despesas_enriquecidas (
    cnpj,
    razao_social,
    trimestre,
    ano,
    valor_despesas,
    registro_ans,
    modalidade,
    uf
)
FROM '/caminho/para/consolidado_despesas_enriquecido.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';


-- 3) Importar dados agregados (2.3)
COPY despesas_agregadas (
    razao_social,
    uf,
    total_despesas,
    media_despesas,
    desvio_padrao
)
FROM '/caminho/para/despesas_agregadas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
