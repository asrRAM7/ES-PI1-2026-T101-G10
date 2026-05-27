create database if not exists eleicao_db;
use eleicao_db;
create table candidatos(
id_candidato int primary key auto_increment, 
nome_candidato varchar(50) NOT NULL,
numero_votacao int UNIQUE,
partido varchar(50) NOT NULL 
);

create table eleitores(
id_eleitor int primary key auto_increment,
nome_eleitor varchar(50) NOT NULL,
titulo_eleitor varchar(12) NOT NULL UNIQUE,
cpf varchar(11) NOT NULL UNIQUE,
mesario INT NOT NULL,
chave_acesso VARCHAR(10),
);

create table votos(
id_voto INT PRIMARY KEY auto_increment,
id_eleitor INT NOT NULL, 
id_candidato INT, 
protocolo_votacao VARCHAR(12) NOT NULL UNIQUE,
data_votacao DATETIME default current_timestamp,
foreign key (id_eleitor) REFERENCES (id_eleitor),
foreign key (id_candidato) REFERENCES (id_candidato)
)

SELECT * FROM eleitores;
// INSERT INTO eleicao_db.candidatos (nome_candidato,numero_votacao,partido)
// VALUES ('Manuel',14,'Partido dos Aposentados');