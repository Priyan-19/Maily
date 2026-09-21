from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.email import router as email_router
from app.api.routes.analysis import router as analysis_router
from app.api.routes.digest import router as digest_router
from app.api.routes.preference import router as preference_router
from app.workers.scheduler import (
    start_scheduler,
    stop_scheduler,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        from app.core.database import engine, Base
        import app.models  # ensure models are registered
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        print(f"Database table initialization warning: {exc}")

    try:
        start_scheduler()
    except Exception as exc:
        print(f"Scheduler startup warning: {exc}")

    yield

    stop_scheduler()

app = FastAPI(
    title="Maily API",
    description="AI-powered email assistant",
    version="0.1.0",
    lifespan=lifespan,
    
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(email_router)
app.include_router(analysis_router)
app.include_router(digest_router)
app.include_router(preference_router)



@app.get("/")
def root():
    return {
        "message": "Maily API is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }