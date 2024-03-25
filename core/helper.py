from passlib.context import CryptContext
from .constant import  KEY_CRYPT
from cryptography.fernet import Fernet
import base64
import os

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

key_text= KEY_CRYPT

# In khóa Fernet mới
key_base64 = key_text.encode('utf-8')

print(key_base64)
# Khởi tạo cipher suite với khóa từ chuỗi văn bản
cipher_suite = Fernet(key_base64)

def hash(string):
    return crypt_context.hash(string)
def verifyHash(string, hash_code):
    return crypt_context.verify(string, hash_code)

# Mã hóa dữ liệu
def encrypt(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Giải mã dữ liệu
def decrypt(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data


def get_subdirectories(path, excluded_names=None):
    # Lấy tất cả các tệp và thư mục trong thư mục hiện tại
    contents = os.listdir(path)
    subdirectories = []
    for item in contents:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and item not in excluded_names and not item.startswith('.'):
            subdirectories.append(item)
    return subdirectories
