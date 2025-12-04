CREATE DATABASE IF NOT EXISTS taskflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE taskflow_db;


CREATE TABLE usuarios (
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE KEY,
    senha_hash VARCHAR(255) NOT NULL,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


CREATE TABLE tarefas (
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	usuario_id INT UNSIGNED NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NULL,
    status ENUM('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA') NOT NULL DEFAULT 'PENDENTE',
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    concluido_em DATETIME NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE INDEX idx_usuario_id ON tarefas(usuario_id);
CREATE INDEX idx_usuario_id_status ON tarefas(usuario_id, status);
CREATE INDEX idx_criado_em ON tarefas(criado_em);


/*INSERT INTO usuarios(nome, email, senha_hash)
VALUES ('Cleiton Silva', 'cleitonsilva@gmail.com', 'hashcleiton');

INSERT INTO tarefas (usuario_id, titulo, descricao, status)
VALUES (1, 'Arrumar a casa', 'Fazer uma faxina completa na casa para receber visitas', 'PENDENTE');
INSERT INTO tarefas (usuario_id, titulo, descricao, status, concluido_em)
VALUES (1, 'Viajar para a praia', 'Arrumar as malas e preparar o carro para viajar para a praia', 'CONCLUIDA', NOW());

UPDATE tarefas SET status = 'EM_ANDAMENTO' WHERE id = 1;
UPDATE tarefas SET status = 'CANCELADA' WHERE id = 2;

SELECT * FROM tarefas 
WHERE usuario_id = 1
ORDER BY criado_em DESC*/
