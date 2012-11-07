set character_set_database=UTF8;
drop database if exists oldprojects;
create database oldprojects character set 'UTF8';
grant all on oldprojects.* to 'puser'@'%' identified by 'pu8549';
use oldprojects;

CREATE TABLE IF NOT EXISTS Projects(
	IdProject INT AUTO_INCREMENT, 
    Code CHAR(5) not null, 
    Description varchar(80) not null,
    PRIMARY KEY(IdProject)
) ENGINE=INNODB character set utf8;

CREATE TABLE IF NOT EXISTS Resources(
	IdResource INT AUTO_INCREMENT, 
    Name VARCHAR(50) not null, 
    Cost real,
    PRIMARY KEY(IdResource)
) ENGINE=INNODB character set utf8;

CREATE TABLE IF NOT EXISTS Tasks(
	IdTask INT AUTO_INCREMENT,
	IdProjectParent INT NOT NULL,
	IdTaskParent INT,
	Task VARCHAR(150),
	PRIMARY KEY(IdTask),
	foreign key(IdProjectParent)
	references Projects(IdProject)
	on update cascade
) ENGINE=INNODB character set utf8;

CREATE TABLE IF NOT EXISTS Activities(
	IdActivity INT AUTO_INCREMENT, 
    Activity VARCHAR(45) not null, 
    PRIMARY KEY(IdActivity)
) ENGINE=INNODB character set utf8;

CREATE TABLE IF NOT EXISTS Entries(
	IdEntry INT AUTO_INCREMENT,
	IdResource INT NOT NULL,
	IdProject int not null,
	IdTask int,
	IdActivity int not null,
	Tsec real not null,
	creation_time DATETIME NULL,
	update_time DATETIME NULL,
	primary key(IdEntry),
	foreign key(IdResource)
	references Resources(IdResource)
	on update cascade
	on delete cascade,
	foreign key(IdProject) 
	references Projects(IdProject)
	on update cascade
	on delete cascade,
	foreign key(IdActivity)
	references Activities(IdActivity)
	on update cascade
	on delete cascade
) engine=innodb character set utf8;


delimiter |
CREATE TRIGGER Entry_INSERT BEFORE INSERT ON Entries
for each row begin
	set new.creation_time = now();
	set new.update_time = now();
end;

CREATE TRIGGER Entry_UPDATE BEFORE UPDATE ON Entries
for each row begin
	set new.update_time = now();
end;
|
delimiter ;
