create database projeto;
use projeto;
create table candidatos(
id int primary key, 
nome varchar(50), 
partido varchar(10)
);
create table eleitores(
id int primary key auto_increment,
nome varchar(50) NOT NULL,
titulo varchar(12) NOT NULL,
CPF varchar(11) NOT NULL,
mesario int NOT NULL
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
