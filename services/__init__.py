import os
import sys
from importlib import import_module
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
CURRENT_FOLDER_NAME = os.path.basename(os.path.dirname(FOLDER_PATH))
# Thêm đường dẫn của thư mục  vào sys.path
sys.path.append(BASE_DIR)
sys.path.append(FOLDER_PATH)


# Lấy danh sách tất cả các file trong thư mục 
module_files = [f[:-3] for f in os.listdir(FOLDER_PATH) if f.endswith('.py') and f != '__init__.py']

# Import tất cả các class model từ các file trong thư mục
for module_file in module_files:
    module = import_module(f'{CURRENT_FOLDER_NAME}.{module_file}')
    classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
    print({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__}, 'model_init')
    globals().update({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})

