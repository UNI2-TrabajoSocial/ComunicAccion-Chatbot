import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Configuración de la base de datos desde variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Sin SSL en desarrollo
SQLALCHEMY_ENGINE_OPTIONS = {}

# Configuración de webhook / WhatsApp
VERIFY_TOKEN   = os.getenv('VERIFY_TOKEN')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_URL   = os.getenv('WHATSAPP_URL')
