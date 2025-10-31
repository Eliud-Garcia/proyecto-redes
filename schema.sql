CREATE TABLE IF NOT EXISTS eventos (
    id SERIAL PRIMARY KEY,
    creador VARCHAR(100),
    nombre VARCHAR(200),
    fecha DATE,
    hora TIME,
    descripcion TEXT,
    imagen VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE
);

-- Verificar los datos
SELECT * FROM eventos;
