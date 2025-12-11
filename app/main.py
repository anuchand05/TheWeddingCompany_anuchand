from fastapi import FastAPI
from .routers import orgs, admin

app = FastAPI(title="Organization Management Service")
app.include_router(orgs.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"msg": "Org Management Service running"}
