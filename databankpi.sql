create database eleicao_db;
use eleicao_db;
create table candidatos(
id_candidato int primary key auto_increment, 
nome_candidato varchar(50),
numero_votacao int,
partido varchar(50)
);
create table eleitores(
id_eleitor int primary key auto_increment,
nome_eleitor varchar(50) NOT NULL,
titulo_eleitor varchar(12) NOT NULL,
cpf varchar(11) NOT NULL,
mesario int NOT NULL,
chave_acesso VARCHAR(10)
);

SELECT * FROM eleitores;
