drop database if exists proyectos;
create database proyectos character set 'UTF8';
grant all on proyectos.* to 'puser'@'localhost';
use proyectos;

CREATE TABLE IF NOT EXISTS Proyectos(
	IdProyecto INT AUTO_INCREMENT, 
    Codigo CHAR(3) not null, 
    Descripcion varchar(45) not null,
    PRIMARY KEY(IdProyecto)
) ENGINE=INNODB character set utf8;

CREATE TABLE IF NOT EXISTS Recursos(
	IdRecurso INT AUTO_INCREMENT, 
    Nombre VARCHAR(45) not null, 
    Coste real,
    PRIMARY KEY(IdRecurso)
) ENGINE=INNODB character set utf8;


CREATE TABLE IF NOT EXISTS Fases(
	IdFase INT AUTO_INCREMENT, 
    Fase VARCHAR(45) not null, 
    PRIMARY KEY(IdFase)
) ENGINE=INNODB character set utf8;

CREATE TABLE IF NOT EXISTS Cargas(
	IdCarga INT AUTO_INCREMENT,
	IdRecurso INT NOT NULL,
	IdProyecto int not null,
	IdFase int not null,
	segundos real not null,
	creation_time DATETIME NULL,
	update_time DATETIME NULL,
	primary key(IdCarga),
	foreign key(IdRecurso)
	references Recursos(IdRecurso)
	on update cascade
	on delete cascade,
	foreign key(IdProyecto) 
	references Proyectos(IdProyecto)
	on update cascade
	on delete cascade,
	foreign key(IdFase)
	references Fases(IdFase)
	on update cascade
	on delete cascade
) engine=innodb character set utf8;


delimiter |
CREATE TRIGGER Carga_INSERT BEFORE INSERT ON Cargas
for each row begin
	set new.creation_time = now();
	set new.update_time = now();
end;

CREATE TRIGGER Carta_UPDATE BEFORE UPDATE ON Cargas
for each row begin
	set new.update_time = now();
end;
|
delimiter ;

load data infile '/Users/bicho/restec/sql_creacion_db/proyectos.txt' into table proyectos fields terminated by '\t' (Codigo, Descripcion) set IdProyecto = NULL;

