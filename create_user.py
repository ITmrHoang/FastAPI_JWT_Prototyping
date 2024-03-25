import argparse

from models import User
from core import SessionLocal
session = SessionLocal()
def create_user(username, password, email, is_supper_admin):
    # Tạo một đối tượng User mới
    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.hashed_password=password
    new_user.is_active=True
    new_user.is_supper_admin=is_supper_admin
    print('hashed_password', new_user.__dict__)
    # Lưu người dùng vào cơ sở dữ liệu
    session.add(new_user)
    session.commit()
    session.close()


if __name__ == "__main__":
    # Tạo một đối tượng ArgumentParser
    parser = argparse.ArgumentParser(description="Create a user")


    # Thêm các tham số dòng lệnh
    parser.add_argument("-u", "--username", help="Username of the user to create")
    parser.add_argument("-p", "--password", help="Password of the user to create")
    parser.add_argument("-e", "--email", help="Email of the user to create")
    parser.add_argument("-su", "--supperadmin", action='store_true', help="user is supper admin -flag when create supper admin")

    # Parse các tham số dòng lệnh
    args = parser.parse_args()
    
    if not args.username:
        args.username = input("Enter username: ")

    # Nếu không có mật khẩu được cung cấp, yêu cầu người dùng nhập
    if not args.password:
        check = True
        while(check):
            password = input("Enter password: ")
            confirm_password = input("Enter confirm password: ")
            if(password == confirm_password):
                args.password = password
                check = False

    # Nếu không có email được cung cấp, yêu cầu người dùng nhập
    if not args.email:
        args.email = input("Enter email: ")
    # Gọi hàm tạo người dùng với tên người dùng, mật khẩu và email đã được cung cấp
        
    create_user(args.username, args.password, args.email, args.supperadmin)