from fastapi import FastAPI, Depends
from app.routes.auth import router as auth_router
from app.auth import get_current_user
from app.schemas import UserOut
from app.models import User
from app.routes.applications import router as applications_router


app = FastAPI(title="Job Tracker API", version="1.0.0")
app.include_router(auth_router)
app.include_router(applications_router)


@app.get("/")
def root():
    return {"name": "Job Tracker API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
