# Notas

# Ver certificado en algun servidor con base de datos mysql, descargarlo y ponerlo en la carpeta raíz del proyecto.
# Usar glitch https://glitch.com/, para pruebas.
# En glitch crear las variables de entorno de acuerdo a las credenciales y tokens de meta for developers en la app creada.


# En el sett.py puede ser así también:
#############################################################################################
import os
from dotenv import load_dotenv

# carga .env
load_dotenv()

# configuración de la base de datos
DB_USER = os.getenv('DB_USER', 'USUARIO BD')
DB_PASS = os.getenv('DB_PASSWORD', 'PASSWOR DE LA BASE DE DATOS')
DB_HOST = os.getenv('DB_HOST', 'HOST SEL SERVIDOR DE LA BASE DE DATOS')
DB_PORT = os.getenv('DB_PORT', 'ACÁ VA EL PUERTO')
DB_NAME = os.getenv('DB_NAME', 'NOMBRE DE LA BASE DE DATOS')

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Sin SSL en desarrollo
SQLALCHEMY_ENGINE_OPTIONS = {}

# configuración de webhook / WhatsApp
VERIFY_TOKEN   = os.getenv('VERIFY_TOKEN', 'TOKEN DEFINIDO EN EL PROYECTO')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN', '')
WHATSAPP_URL   = os.getenv('WHATSAPP_URL', '')
#############################################################################################

