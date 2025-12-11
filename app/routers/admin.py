from fastapi import APIRouter, HTTPException
from ..schemas import AdminLoginRequest, TokenResponse
from ..db import admins_col
from ..auth import verify_password, create_access_token
from ..config import settings

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/login", response_model=TokenResponse)
async def admin_login(payload: AdminLoginRequest):
    admin = await admins_col.find_one({"email": payload.email})
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(payload.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_data = {"admin_email": admin["email"], "organization_name": admin["organization_name"], "admin_id": str(admin["_id"])}
    token = create_access_token(token_data)
    return {"access_token": token}
