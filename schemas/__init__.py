import os
import sys
from importlib import import_module
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
CURRENT_FOLDER_NAME = os.path.basename(FOLDER_PATH)
# Thêm đường dẫn của thư mục  vào sys.path
sys.path.append(BASE_DIR)
# sys.path.append(FOLDER_PATH)

# # Lấy danh sách tất cả các file trong thư mục 
# module_files = [f[:-3] for f in os.listdir(FOLDER_PATH) if f.endswith('.py') and f != '__init__.py']
# # # Import tất cả các class model từ các file trong thư mục hiện tại
# for module_file in module_files:
#     module = import_module(f'{CURRENT_FOLDER_NAME}.{module_file}')
#     classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
#     # print(module_file, '---', module,  'classlist',classes, classes[-1].__module__)
# #     # print(classes, 'init\n')
# #     # for cls in classes:
# #     #     print(module_file, 'clss', cls.__module__, module.__name__, sep=' 00  ---- ----00')
#     globals().update({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})


## load class toàn bộ class trong folder hiện tại và sub folder của nó
def get_path_module(directory):
    path_list = []
    for root, dirs, files in os.walk(directory):
        base_name = os.path.basename(root)
        if base_name == "__pycache__": continue 
        file_name_list = [ f for f in files if f.endswith('.py') and f != '__init__.py']
        for f in file_name_list:
            path = os.path.join(root,f)
            path_list.append(path)
        # for file in files:
            # file_path = os.path.join(root, file)
            # files_list.append(file_path)
    # remove base path
    result = []
    for path in path_list:
        # # Sử dụng str.replace()
        # relative_path = path.replace(root_folder, '')

        # # Hoặc sử dụng str.split()
        # relative_path = path.split(root_folder)[1]
        relative_path = os.path.relpath(path, BASE_DIR)
        ## os.sep là hằng số ký tự phân cách tương ứng với hệ điều hành
        str_module = relative_path[:-3].replace(os.sep, ".")
        result.append(str_module)
    return result

path_module = get_path_module(FOLDER_PATH)

for module_path in path_module:
    try:
        module = import_module(f'{module_path}')
        classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
        globals().update({cls.__name__: cls for cls in classes if cls.__module__ == module.__name__})
    except Exception as e:
        print(f'load module {__file__} error: - {e}')