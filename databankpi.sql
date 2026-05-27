create database eleicao_db;
use eleicao_db;
create table if not exists candidatos(
id_candidato int primary key auto_increment, 
nome_candidato varchar(50),
numero_votacao int,
partido varchar(50)
);

create table if not exists eleitores(
id_eleitor int primary key auto_increment,
nome_eleitor varchar(50) NOT NULL,
titulo_eleitor varchar(12) NOT NULL UNIQUE,
cpf varchar(12) NOT NULL UNIQUE,
mesario int NOT NULL,
chave_acesso VARCHAR(10),
votou int
);

create table if not exists votos(
voto INT,
protocolo_votacao VARCHAR(15),
data_votacao DATETIME,
foreign key (voto) REFERENCES candidatos(numero_votacao)
)

# SELECT * FROM eleitores;
# DROP TABLE eleitores;