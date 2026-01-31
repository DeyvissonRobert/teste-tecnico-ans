-- Query 1

WITH despesas_por_trimestre AS (
    SELECT
        cnpj,
        razao_social,
        CONCAT(ano, '-', trimestre) AS periodo,
        SUM(valor_despesas) AS total_despesas
    FROM despesas_consolidadas
    GROUP BY cnpj, razao_social, ano, trimestre
),

primeiro_ultimo AS (
    SELECT
        cnpj,
        razao_social,
        MIN(periodo) AS primeiro_periodo,
        MAX(periodo) AS ultimo_periodo
    FROM despesas_por_trimestre
    GROUP BY cnpj, razao_social
),

valores_extremos AS (
    SELECT
        p.cnpj,
        p.razao_social,
        d1.total_despesas AS despesas_inicial,
        d2.total_despesas AS despesas_final
    FROM primeiro_ultimo p
    JOIN despesas_por_trimestre d1
        ON d1.cnpj = p.cnpj
       AND d1.periodo = p.primeiro_periodo
    JOIN despesas_por_trimestre d2
        ON d2.cnpj = p.cnpj
       AND d2.periodo = p.ultimo_periodo
    WHERE d1.total_despesas > 0
)

SELECT
    cnpj,
    razao_social,
    despesas_inicial,
    despesas_final,
    ROUND(
        ((despesas_final - despesas_inicial) / despesas_inicial) * 100,
        2
    ) AS crescimento_percentual
FROM valores_extremos
ORDER BY crescimento_percentual DESC
LIMIT 5;

-- Query 2
-- Distribuição de despesas por UF
-- Retorna os 5 estados com maiores despesas totais
-- Inclui a média de despesas por operadora em cada UF

SELECT
    uf,
    SUM(valor_despesas) AS total_despesas_uf,
    AVG(valor_despesas) AS media_despesas_por_operadora
FROM despesas_consolidadas
WHERE uf IS NOT NULL
GROUP BY uf
ORDER BY total_despesas_uf DESC
LIMIT 5;

-- Query 3

WITH media_geral AS (
    SELECT AVG(valor_despesas) AS media_despesas
    FROM despesas_consolidadas
),

despesas_acima_media AS (
    SELECT
        cnpj,
        trimestre,
        ano,
        valor_despesas
    FROM despesas_consolidadas d
    CROSS JOIN media_geral m
    WHERE d.valor_despesas > m.media_despesas
),

contagem_trimestres AS (
    SELECT
        cnpj,
        COUNT(DISTINCT CONCAT(ano, trimestre)) AS qtd_trimestres_acima_media
    FROM despesas_acima_media
    GROUP BY cnpj
)

SELECT
    COUNT(*) AS total_operadoras
FROM contagem_trimestres
WHERE qtd_trimestres_acima_media >= 2;
