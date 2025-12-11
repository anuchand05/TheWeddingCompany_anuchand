from fastapi import FastAPI
from .routers import orgs, admin
from fastapi.responses import RedirectResponse

app = FastAPI(title="Organization Management Service")
app.include_router(orgs.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
