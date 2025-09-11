# IMPORTANTE
## si clonas el repositorio borra la carpeta venv
esto es para que lo configures con los siguientes pasos para evitar problemas

sudo apt update
sudo apt install -y python3 python3-venv python3-pip

# crear entorno virtual
python3 -m venv venv

# activarlo
source venv/bin/activate

# actualizar pip dentro de env
pip install --upgrade pip


# instala dependencias del proyecto
pip install flask psycopg2-binary
pip install pillow


# ejecuta
python app.py

# desactivar el env
deactivate