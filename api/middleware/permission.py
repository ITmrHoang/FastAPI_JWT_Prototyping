from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from functools import wraps

api_key_header = APIKeyHeader(name="Authorization")

def check_permission(resource_id):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = await api_key_header.__call__(args[0])  # Assume the token is passed as a header
            # Perform your permission check here based on the token and resource_id
            if not has_permission(token, resource_id):
                raise HTTPException(status_code=403, detail="Permission denied")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

async def has_permission(token, resource_id):
    # Your logic to check if the token has permission for the specified resource_id
    return True