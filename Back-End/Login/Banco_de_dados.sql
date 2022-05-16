create database marketplace;
use marketplace;
create table logins (
USER_ID int(4) auto_increment primary key,
Email varchar(40) not null unique,
Senha varchar(30) not null
);
describe logins;
select * from logins;
