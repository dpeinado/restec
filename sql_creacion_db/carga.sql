CREATE TABLE IF NOT EXISTS Cargas(
	IdCarga INT AUTO_INCREMENT,
	IdRecurso INT NOT NULL,
	IdProyecto int not null,
	IdFase int not null,
	horas real not null,
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
) engine=innodb;

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

insert into Cargas(IdRecurso,IdProyecto,IdFase,horas) values('1','2','2','33.5');
insert into Cargas(IdRecurso,IdProyecto,IdFase,horas) values('2','1','1','3.5');
insert into Cargas(IdRecurso,IdProyecto,IdFase,horas) values('1','2','2','4.5');
insert into Cargas(IdRecurso,IdProyecto,IdFase,horas) values('1','3','3','13.5');