from fastapi import APIRouter, HTTPException, Depends, Header
from ..schemas import CreateOrgRequest, OrgResponse, UpdateOrgRequest
from ..db import orgs_col, admins_col, master_db
from ..auth import hash_password, verify_password, create_access_token
from ..config import settings
from typing import Optional
import re

router = APIRouter(prefix="/org", tags=["org"])

def safe_collection_name(name: str) -> str:
    # sanitize: lowercase, alphanum and underscore
    s = re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()
    return f"org_{s}"

@router.post("/create", response_model=OrgResponse)
async def create_org(payload: CreateOrgRequest):
    org_name = payload.organization_name.strip()
    existing = await orgs_col.find_one({"organization_name": org_name})
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    collection_name = safe_collection_name(org_name)
    # create a dynamic collection (Mongo creates on first insert; we can create by ensuring index or inserting init doc)
    org_collection = master_db[collection_name]
    # optional initialization (empty doc then delete)
    await org_collection.insert_one({"_init": True})
    await org_collection.delete_many({"_init": True})

    # create admin
    hashed = hash_password(payload.password)
    admin_doc = {
        "email": payload.email,
        "password": hashed,
        "organization_name": org_name,
        "collection_name": collection_name
    }
    admin_result = await admins_col.insert_one(admin_doc)
    org_doc = {
        "organization_name": org_name,
        "collection_name": collection_name,
        "admin_ref": admin_result.inserted_id,
        "created_at": __import__("datetime").datetime.utcnow()
    }
    await orgs_col.insert_one(org_doc)
    return OrgResponse(organization_name=org_name, collection_name=collection_name, admin_email=payload.email)


@router.get("/get", response_model=OrgResponse)
async def get_org(organization_name: str):
    org = await orgs_col.find_one({"organization_name": organization_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    # lookup admin email
    admin = await admins_col.find_one({"_id": org["admin_ref"]})
    admin_email = admin["email"] if admin else ""
    return OrgResponse(organization_name=org["organization_name"], collection_name=org["collection_name"], admin_email=admin_email)

# Helper dependency: simple token-based admin auth for delete and update
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = __import__("jwt").decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    # payload should contain admin_email and organization_name
    return payload

@router.put("/update")
async def update_org(payload: UpdateOrgRequest, token_payload: dict = Depends(get_current_admin)):
    # Ensure authenticated admin belongs to organization
    if token_payload.get("organization_name") != payload.organization_name:
        raise HTTPException(status_code=403, detail="Not authorized to update this org")

    org = await orgs_col.find_one({"organization_name": payload.organization_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # If new org name provided, ensure no conflict
    updates = {}
    if payload.new_organization_name:
        newname = payload.new_organization_name.strip()
        if await orgs_col.find_one({"organization_name": newname}):
            raise HTTPException(status_code=400, detail="New organization name already exists")
        new_collection = safe_collection_name(newname)
        old_collection = org["collection_name"]
        # rename collection: Mongo supports renameCollection across DBs; here same DB
        db = master_db
        await db[old_collection].rename(new_collection, dropTarget=True)
        updates["organization_name"] = newname
        updates["collection_name"] = new_collection
        # update admin docs referencing collection / name
        await admins_col.update_many({"organization_name": payload.organization_name}, {"$set":{"organization_name": newname, "collection_name": new_collection}})
    if payload.email or payload.password:
        # update admin (the authenticated admin)
        admin_email = token_payload.get("admin_email")
        admin = await admins_col.find_one({"email": admin_email, "organization_name": updates.get("organization_name", payload.organization_name)})
        if not admin:
            raise HTTPException(status_code=404, detail="Admin profile not found")
        admin_updates = {}
        if payload.email:
            admin_updates["email"] = payload.email
        if payload.password:
            admin_updates["password"] = hash_password(payload.password)
        if admin_updates:
            await admins_col.update_one({"_id": admin["_id"]}, {"$set": admin_updates})
    if updates:
        await orgs_col.update_one({"_id": org["_id"]}, {"$set": updates})
    return {"status": "ok", "updated": updates}

@router.delete("/delete")
async def delete_org(organization_name: str, token_payload: dict = Depends(get_current_admin)):
    if token_payload.get("organization_name") != organization_name:
        raise HTTPException(status_code=403, detail="Not authorized to delete this org")
    org = await orgs_col.find_one({"organization_name": organization_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    collection_name = org["collection_name"]
    # drop collection
    await master_db[collection_name].drop()
    # remove admin(s)
    await admins_col.delete_many({"organization_name": organization_name})
    # remove org metadata
    await orgs_col.delete_one({"_id": org["_id"]})
    return {"status": "deleted"}
