# REQUISITOS

Para poder ejecutar este pequeño proyecto debes tener instalado lo siguiente:
* Python 
* Postgres

puedes instalar python con los siguientes comandos
```sh
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

Durante el desarrollo se trabajó en Ubuntu, las versiones usadas exactamente son las siguientes:
* Python 3.12.3 
* psql (PostgreSQL) 17.6 (Ubuntu 17.6-1.pgdg24.04+1) 



para poder usar este proyecto solo basta con clonar el repositorio usando el comando git clone.
una vez clonado vamos a la carpeta que contiene el proyecto y usando una terminal colocamos los siguientes comandos.

## crear entorno virtual
```sh
python3 -m venv venv
```


## activarlo

```sh
source venv/bin/activate
```

## actualizar pip dentro de env

```sh
pip install --upgrade pip
```

## instala dependencias del proyecto
```sh
pip install flask psycopg2-binary
pip install pillow

```

## ejecuta
```sh
python3 app.py
```

## desactivar el env
```sh
deactivate
```