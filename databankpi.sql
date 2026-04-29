create database eleicao_db;
use eleicao_db;
create table candidatos(
id_candidato int primary key auto_increment, 
nome_candidato varchar(50),
numero_votacao int,
partido varchar(10)
);
create table eleitores(
id_eleitor int primary key auto_increment,
nome_eleitor varchar(50) NOT NULL,
titulo_eleitor varchar(12) NOT NULL,
cpf varchar(11) NOT NULL,
mesario int NOT NULL,
chave_acesso VARCHAR(10)
);

alter table candidatos
modify column partido varchar(10),
modify column nome varchar(50) NOT NULL;

alter table candidatos 
modify column id int auto_increment;

DELETE from candidatos 
WHERE nome = 'carlos' and partido = 'pt';

alter table candidatos
modify column partido varchar(50);

INSERT into candidatos (nome, partido)
VALUES("Marcos Alberto", "Partido Falso");

INSERT into eleitores (nome, titulo, CPF, mesario)
VALUES ("Maria Silva", 154327169871, 87537822814, 1);
