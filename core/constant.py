from dotenv import load_dotenv
import os
from decouple import config
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR =  Path(__file__).parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

KEY_CRYPT = os.environ.get("KEY_CRYPT", '')

APP_NAME = os.environ.get('APP_NAME',"HIMO")

# openssl rand -hex 32 or your key
SECRET_KEY = "VsiemVNCSGloablHimo@%!)!((&))"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60