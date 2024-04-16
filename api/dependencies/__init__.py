from fastapi import Header,HTTPException, JsonResponse
from utils import errorResponse
async def check_header_has_authorization(Authorizationa: str = Header(None)):
    if Authorizationa is None:
            raise HTTPException(
                status_code=401,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": 'failtoauthorize'},
            )
            # return errorResponse("dont have authorization", status_code = 401)
    return Authorizationa
