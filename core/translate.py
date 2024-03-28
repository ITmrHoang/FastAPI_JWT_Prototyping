import glob
import json
from .constant import BASE_DIR
import os

PATH_LANGUASGES_FOLDER = os.path.join(BASE_DIR, 'languages')
default_languages = 'en'
languages = {}

language_list = glob.glob(f"{PATH_LANGUASGES_FOLDER}/*.json")

for path_file in language_list:

    filename = os.path.basename(path_file)

    lang_code = filename.split('.')[0]

    with open(path_file, 'r', encoding='utf8') as file:

        languages[lang_code] = json.load(file)