#!/bin/bash


# Tạo một đoạn string ngẫu nhiên gồm 11 ký tự
random_string=$(head /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 43)

# Giá trị mới bạn muốn gán cho keya_app
KEY_CRYPT="KEY_CRYPT=$random_string="
# Tên tệp tin
file_path=".env"


# Kiểm tra xem có tồn tại key_app trong tệp không
if grep -q "^KEY_CRYPT=" "$file_path"; then
    if grep -q "^KEY_CRYPT=$" "$file_path"; then
        echo "KEY_CRYPT đã tồn tại nhưng không có giá trị."
        # Thêm giá trị mới vào dòng KEY_APP
        sed -i "s/^KEY_CRYPT=.*$/$KEY_CRYPT/" "$file_path"
    else
       echo "KEY_CRYPT đã được tạo trước đó"
    fi
else
    # Nếu không tồn tại, thêm vào đầu tệp
    cho "chèn thêm mới KEY_CRYPT"
    sed -i "1i$KEY_CRYPT" "$file_path"
fi