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


CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol VARCHAR(20) DEFAULT 'usuario'  -- puede ser 'usuario' o 'admin'
);


-- Verificar los datos
SELECT * FROM eventos;
SELECT * FROM usuarios;
