create database proyectoparqueo

use proyectoparqueo
go

-- crear tabla usuario

create table usuarios
(	id_usuario int primary key identity(1,1),
	cedula varchar(20),
	nombre varchar(100),
	telefono varchar(20),
	direccion varchar(200),
)

-- crear tabla vehiculo

create table vehiculos
(
	id int identity(100,1) primary key,
	placa varchar(8) not null,
	marca varchar(50) not null,
	modelo varchar(200) not null,
	id_usuario int,
	foreign key (id_usuario) references usuarios(id_usuario)
)

-- crear tabla reservas


create table reservas
(
	id_reservas int primary key identity(1,1),
	id_vehiculo int,
	fecha date,
	hora_entrada time,
	hora_salida time,
	espacio varchar(10),
	foreign key (id_vehiculo) references vehiculos(id),
	
);

-- agregar restriccion 
alter TABLE reservas,
ADD CONSTRAINT UQ_reserva_espacio_fecha UNIQUE (fecha, espacio);

SELECT fecha, espacio, COUNT(*) AS cantidad
FROM reservas
GROUP BY fecha, espacio
HAVING COUNT(*) > 1;


-- crear tabla de historial

create table historial(
	id_historial int primary key identity(1,1),
	id_vehiculo int,
	hora_entrada datetime,
	hora_salida datetime,
	foreign key (id_vehiculo) references vehiculos(id)
)

-- crear tabla stack

create table valet_stack (
    id_stack int primary key identity(1,1),
    id_vehiculo int NOT NULL,
    posicion int NOT NULL, -- 1 es el fondo de la pila, el más antiguo
    fecha_entrada datetime default getdate(),
    fecha_salida datetime NULL,
    foreign key (id_vehiculo) references vehiculos(id)
);


-- crear tabla de pendientes


CREATE TABLE pendientes (
    id_pendiente INT PRIMARY KEY IDENTITY(1,1),
    id_vehiculo INT,
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(id_vehiculo) REFERENCES vehiculos(id)
);

-- crear tabla de factura
create table factura (
	id_factura int identity(1,1) primary key,
	fecha datetime default getdate(),
	idvehiculo int not null,
	montoapagar money,
	foreign key(idvehiculo) references vehiculos(id)
	)

