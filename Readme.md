# Using docker-compose
  ``` docker compose up -d ```
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

# format data
## in models 
### format by getJSon()
``` @override
 def getJson(self) -> instance: # format data 
      item = self.to_dict()
      return item
```

### format by to_dict() : function using fields in model to dict data,you can't edit this. return self will dont get relationships

``` 
def to_dict(self, includes= None, excludes= []):
        attrs = [
                  attr for attr in dir(self) \
                  if not attr.startswith("_") and not callable(getattr(self, attr)) \
                    and (attr != 'metadata') and (attr != 'registry') and attr not in excludes ] \
                if includes is None else includes 
        return { column: getattr(self, column) for column in attrs}
```
# infor package
 [x] setting env by: [decouple](https://pypi.org/project/python-decouple/)




