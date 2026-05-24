-- DROP DATABASE IF EXISTS TRABALHO;

CREATE DATABASE IF NOT EXISTS TRABALHO
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE TRABALHO;
-- DROP TABLE IF EXISTS funcoes;
CREATE TABLE IF NOT EXISTS livros (
    id_livro BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    genero ENUM('Terror', 'Ficção', 'Romance', 'Aventura') DEFAULT 'Ficção',
    ano INT,
    paginas INT,
    sinopse TEXT,
    perm_cadastrar BOOLEAN DEFAULT 0,
    perm_editar BOOLEAN DEFAULT 0,
    perm_excluir BOOLEAN DEFAULT 0,
    perm_listar BOOLEAN DEFAULT 0,

    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
-- a partir daqui é uma tentativa
 
-- DROP TABLE IF EXISTS clientes;
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    numero INT NOT NULL,
    email VARCHAR(100),
    pais VARCHAR(30) DEFAULT 'Brasil',
    estado VARCHAR(50),
    cidade VARCHAR(50),
    senha VARCHAR(255),
    descricao VARCHAR(255),
    livros BOOLEAN DEFAULT 0,
    autores BOOLEAN DEFAULT 0,
    usuarios BOOLEAN DEFAULT 0,
    status ENUM('Ativo', 'Inativo') DEFAULT 'Ativo',

    livro_id BIGINT UNSIGNED NOT NULL,

    -- LOGS
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    -- RELACIONAMENTO
    CONSTRAINT fk_usuario_livro
    FOREIGN KEY (livro_id) REFERENCES livros (id_livro)
);

CREATE TABLE IF NOT EXISTS autores (
    id_autor BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50) NOT NULL,
    nascimento DATE NOT NULL,
    falecimento DATE DEFAULT NULL,
    biografia TEXT,
    situacao ENUM('Vivo', 'Falecido') DEFAULT 'Vivo',
    genero ENUM('Feminino', 'Masculino', 'Outro') DEFAULT 'Outro',

    -- LOGS
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    alterado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
