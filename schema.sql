CREATE TABLE IF NOT EXISTS categoria (
    id        SERIAL PRIMARY KEY,
    nome      VARCHAR(60) NOT NULL,
    descricao VARCHAR(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_categoria_nome_lower
    ON categoria (lower(nome));

CREATE TABLE IF NOT EXISTS prato (
    id           SERIAL PRIMARY KEY,
    categoria_id INTEGER NOT NULL
                 REFERENCES categoria (id) ON DELETE RESTRICT,
    nome         VARCHAR(100) NOT NULL,
    descricao    VARCHAR(255),
    preco        NUMERIC(10, 2) NOT NULL,
    disponivel   BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_prato_preco_positivo CHECK (preco > 0)
);

CREATE INDEX IF NOT EXISTS ix_prato_categoria_id ON prato (categoria_id);
