-- Comandos para a criação do banco de dados

--(===============================<para MySQL>===============================)--

-- create database marketplace;
-- use marketplace;

---------------------------<Tabela de Logins>---------------------------

-- create table logins (
-- id int(4) auto_increment primary key,
-- Email varchar(40) not null unique,
-- Senha varchar(88) not null
-- );
-- OBS: O campo de senha está com 88 caracteres pois ela é criptografada

---------------------------<Visualizar Dados>---------------------------
-- Descomentar abaixo
-- describe logins;
-- select * from logins;

--(=============================<para PostgreSQL>============================)--

-- Criar database pelo pgadmin sem instruções
-- As instruções estão bugadas

-- create database IF NOT EXISTS marketplace;
-- select testedb;

---------------------------<Tabela de Logins>---------------------------
create table if not exists logins (
id serial,
Email varchar(40) not null unique,
Senha varchar(88) not null
);
-- OBS: O campo de senha está com 88 caracteres pois ela é criptografada

---------------------------<Visualizar Dados>---------------------------
-- describe logins;
-- select * from logins;
