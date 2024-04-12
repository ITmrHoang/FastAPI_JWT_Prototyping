from fastapi import Header, HTTPException
async def check_header_has_authorization(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=400, detail="Authorization dont exist")   
