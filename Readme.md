# Setup environment
## install virtualenv create env
    python -m pip install --user virtualenv
    python -m virtualenv <name_env>

    or

    pip install virtualenv
    virtualenv --python C:\Path\To\Python\python.exe venv

## install 
  ```
  pip install fastapi
  pip install "uvicorn[standard]"

  or 
  pip install requirements.txt
  ```

## run dev
 ### access to env
 `.\vsiem_env\Scripts\activate `
 
 ` uvicorn main:app --reload `

 ` alembic upgrade head `

# infor package
 [x] setting env by: [decouple](https://pypi.org/project/python-decouple/)




