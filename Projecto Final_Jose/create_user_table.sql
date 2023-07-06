CREATE TABLE IF NOT EXISTS jogos(
    id_jogo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT NOT NULL,
    tipo_de_jogo CHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    role CHAR(255) NOT NULL default "user" NOT NULL,
    username CHAR(255) NOT NULL UNIQUE,
    password CHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS perguntas(
    id_pergunta INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT NOT NULL,
    pergunta CHAR(255) NOT NULL,
    fk_id_jogo INT NOT NULL,
    foreign key(fk_id_jogo) references jogos(id_jogo)

);

CREATE TABLE IF NOT EXISTS respostas(
    id_resposta INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    resposta CHAR(255) NOT NULL,
    corrigir BOOLEAN NOT NULL,
    fk_id_pergunta INTEGER NOT NULL,
    foreign key(fk_id_pergunta) references perguntas(id_pergunta)
);

CREATE TABLE IF NOT EXISTS utilizadores_jogos(
    id_utilizador_jogo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    fk_id_utilizador INTEGER NOT NULL,
    fk_id_jogo INTEGER NOT NULL,
    foreign key(fk_id_utilizador) references users(id),
    foreign key(fk_id_jogo) references jogos(id_jogo)
);

CREATE TABLE IF NOT EXISTS analises(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    mensagem CHAR(255) NOT NULL,
    rating INTEGER NOT NULL,
    nome char(255) NOT NULL,
    fk_id_jogo INTEGER NOT NULL,
    foreign key(fk_id_jogo) references jogos(id_jogo)
);

UPDATE users SET role = 'admin' WHERE id=2;

