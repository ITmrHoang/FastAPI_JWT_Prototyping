# Decorator để bọc một phương thức với xử lý ngoại lệ
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            # Gọi phương thức gốc với các đối số được truyền vào
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Xử lý ngoại lệ tại đây, ví dụ: raise e; hoặc return một giá trị mặc định
            raise e  # Ném lại ngoại lệ để xử lý bên ngoài
    return wrapper

# Metaclass để tự động áp dụng decorator cho tất cả các phương thức của lớp
class HandleExceptionsMeta(type):
    def __new__(cls, name, bases, dct):
        # Duyệt qua tất cả các thuộc tính của lớp
        for attr_name, attr_value in dct.items():
            # Kiểm tra xem thuộc tính đó có phải là một phương thức không
            if callable(attr_value):
                # Áp dụng decorator cho phương thức
                dct[attr_name] = handle_exceptions(attr_value)
        return super().__new__(cls, name, bases, dct)

# Định nghĩa lớp cha với metaclass là HandleExceptionsMeta
class MyClass(metaclass=HandleExceptionsMeta):
    def my_method1(self):
        raise ValueError("Error in my_method1!")

    def my_method2(self):
        raise TypeError("Error in my_method2!")

# Định nghĩa lớp con kế thừa từ MyClass
class MySubClass(MyClass):
    def my_method3(self):
        raise IndexError("Error in my_method3!")

# Sử dụng lớp con với các phương thức đã được bọc
my_sub_object = MySubClass()


try:
    my_sub_object.my_method3()
except Exception as e:
    print(f"Caught error in my_method3: {e}")
