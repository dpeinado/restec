CREATE TABLE IF NOT EXISTS Proyectos(
	IdProyecto INT AUTO_INCREMENT, 
    Codigo CHAR(3) not null, 
    Descripcion varchar(45) not null,
    PRIMARY KEY(IdProyecto)
) ENGINE=INNODB;

INSERT INTO Proyectos(Codigo,Descripcion) VALUES('001', 'Torre InNova S');
INSERT INTO Proyectos(Codigo,Descripcion) VALUES('002', 'Tanques InTega');
INSERT INTO Proyectos(Codigo,Descripcion) VALUES('003', 'Criba InCAR 4022');

CREATE TABLE IF NOT EXISTS Recursos(
	IdRecurso INT AUTO_INCREMENT, 
    Nombre VARCHAR(45) not null, 
    Coste real,
    PRIMARY KEY(IdRecurso)
) ENGINE=INNODB;

INSERT INTO Recursos(Nombre,Coste) VALUES('Diego Peinado', '25.0');
INSERT INTO Recursos(Nombre,Coste) VALUES('Israel Durán', '20.0');


CREATE TABLE IF NOT EXISTS Fases(
	IdFase INT AUTO_INCREMENT, 
    Fase VARCHAR(45) not null, 
    PRIMARY KEY(IdFase)
) ENGINE=INNODB;

INSERt INTO Fases(Fase) VALUES ('Diseño preliminar');
INSERt INTO Fases(Fase) VALUES ('Diseño Detallado');
INSERt INTO Fases(Fase) VALUES ('Listados y DXFs');