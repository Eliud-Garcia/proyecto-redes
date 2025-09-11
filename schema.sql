--tabla 
CREATE TABLE IF NOT EXISTS eventos (
    id SERIAL PRIMARY KEY,
    creador VARCHAR(100),
    nombre VARCHAR(200),
    fecha DATE,
    hora TIME,
    descripcion TEXT,
    imagen VARCHAR(300)
);

--se modifico, entonces agregar los cambios
ALTER TABLE eventos ALTER COLUMN imagen TYPE VARCHAR(200);
ALTER TABLE eventos ADD COLUMN activo BOOLEAN DEFAULT TRUE;


--mostrar los eventos
SELECT * FROM eventos;


