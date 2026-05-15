-- DROP DATABASE IF EXISTS TRABALHO;

CREATE DATABASE IF NOT EXISTS TRABALHO
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE TRABALHO;
-- DROP TABLE IF EXISTS funcoes;
CREATE TABLE IF NOT EXISTS funcoes (
    id_funcao BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(20) NOT NULL UNIQUE,
    status ENUM('Ativo', 'Inativo') DEFAULT 'Ativo',
    descrição VARCHAR(255),
    livros BOOLEAN DEFAULT 0,
    autores BOOLEAN DEFAULT 0,
    usuarios BOOLEAN DEFAULT 0,

    -- LOG

    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
-- a partir daqui é uma tentativa
-- DROP TABLE IF EXISTS clientes;
CREATE TABLE IF NOT EXISTS clientes(

    id_cliente BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
    nome VARCHAR(20) NOT NULL UNIQUE,
    cpf INT NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    numero INT NOT NULL,
    email VARCHAR(20), 
    pais DEFAULT 'Brasil',
    estado VARCHAR(20),
    cidade VARCHAR(20),
    senha CHAR(20),
    descrição VARCHAR(255)
    livros BOOLEAN DEFAULT 0,
    autores BOOLEAN DEFAULT 0,
    usuarios BOOLEAN DEFAULT 0,
    status ENUM('Ativo', 'Inativo') DEFAULT 'Ativo',

    funcao_id BIGINT UNSIGNED NOT NULL,

    --LOGS
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP, 
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        ON UPDATE CURRENT_TIMESTAMP

    --CRIA O RELACIONAMENTO ENTRE TABELAS
    CONSTRAINT fk_cliente_funcao
    FOREIGN KEY (funcao_id) REFERENCES funcoes (id_funcao)
    
);