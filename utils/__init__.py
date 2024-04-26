# from .authentication import verify_password, get_password_hash,create_access_token, create_refresh_token
# from .responses import susscessResponse, errorResponse


"""
module utils have
funtions:

def verify_password(plain_password: str, hashed_password:str) -> bool:

"""
#TODO import dyamic functions in module
import os
import sys
from importlib import import_module
import inspect

# Đường dẫn đến thư mục chứa các module
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

# Thêm đường dẫn của thư mục module vào sys.path
sys.path.append(MODULE_DIR)

# Lấy danh sách tất cả các file trong thư mục của module
module_files = [f[:-3] for f in os.listdir(MODULE_DIR) if f.endswith('.py') and f != '__init__.py']

# Import tất cả các hàm từ các file trong thư mục module
for _module_file in module_files:
    try:
        _module = import_module(f'{_module_file}')
        # module_functions = [func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]
        # for func_name in module_functions:
        #     func = getattr(module, func_name)
        #     print(f"Imported function '{func_name}' from module '{module_file}'")
        _module_functions = []
        for _func_name in dir(_module):
            if callable(getattr(_module, _func_name)) and not _func_name.startswith("__"):
                _i_func = getattr(_module, _func_name)
                # kiểm tra chúng trong module hiện tại
                if _module.__name__ == _i_func.__module__:
                    if  isinstance(_i_func, type):
                        globals().update({_func_name: _i_func})
                    if inspect.isfunction(_i_func):
                        # Đặt hàm mới vào một đối tượng có thể gọi
                        setattr(sys.modules[__name__], _func_name, _i_func)
                    # # Gọi hàm mới
                    # function = getattr(sys.modules[__name__], func_name)
                    # function()
                    # NOTE global có thể import funtion và class nên không cần import class dymaic 
                    # print(func_name, module.__name__ + "name modle  " +  i_func.__module__ , type(i_func), sep=' ---   ')
    except Exception as e:
        print(f'load module {__file__} error: - {e}')
    