-- =========================================
-- Tabela de despesas consolidadas (Teste 1.3)
-- =========================================
CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(20) NOT NULL,
    razao_social TEXT NOT NULL,
    trimestre VARCHAR(10) NOT NULL,
    ano INTEGER NOT NULL,
    valor_despesas DECIMAL(18,2) NOT NULL
);

CREATE INDEX idx_despesas_cnpj ON despesas_consolidadas (cnpj);
CREATE INDEX idx_despesas_trimestre ON despesas_consolidadas (trimestre);


-- =========================================
-- Tabela de operadoras (Teste 2.2)
-- =========================================
CREATE TABLE operadoras (
    cnpj VARCHAR(20) PRIMARY KEY,
    registro_ans VARCHAR(20),
    modalidade TEXT,
    uf CHAR(2)
);

CREATE INDEX idx_operadoras_uf ON operadoras (uf);


-- =========================================
-- Tabela de despesas agregadas (Teste 2.3)
-- =========================================
CREATE TABLE despesas_agregadas (
    id SERIAL PRIMARY KEY,
    razao_social TEXT NOT NULL,
    uf CHAR(2),
    total_despesas DECIMAL(18,2),
    media_despesas DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2)
);

CREATE INDEX idx_agregadas_razao_social ON despesas_agregadas (razao_social);
CREATE INDEX idx_agregadas_uf ON despesas_agregadas (uf);
