# REQUISITOS

Para poder ejecutar este pequeño proyecto debes tener instalado lo siguiente:
* Python 
* Postgres

puedes instalar python con los siguientes comandos
```sh
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```


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
python app.py
```

## desactivar el env
```sh
deactivate
```