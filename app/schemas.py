from pydantic import BaseModel, EmailStr, Field

class CreateOrgRequest(BaseModel):
    organization_name: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)

class OrgResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_email: EmailStr

class UpdateOrgRequest(BaseModel):
    organization_name: str
    new_organization_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
