from dotenv import load_dotenv
import os

APP_NAME = os.environ.get('APP_NAME',"HIMO")

# openssl rand -hex 32 or your key
SECRET_KEY = "VsiemVNCSGloablHimo@%!)!((&))"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60