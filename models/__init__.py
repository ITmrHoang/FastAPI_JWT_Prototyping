import os
import sys
from importlib import import_module
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, 'models'))
# Thêm đường dẫn của thư mục models vào sys.path
sys.path.append(MODEL_PATH)
sys.path.append(BASE_DIR)

# Lấy danh sách tất cả các file trong thư mục models
model_files = [f[:-3] for f in os.listdir(MODEL_PATH) if f.endswith('.py') and f != '__init__.py']

# Import tất cả các class model từ các file trong thư mục models
for model_file in model_files:
    module = import_module(f'models.{model_file}')
    classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
    print({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__}, 'model_init')
    globals().update({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})

