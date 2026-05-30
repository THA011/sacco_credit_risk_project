"""Ruiru PCEA SACCO Portal API bootstrap (local dev).

Created: 2026-05-30 — final draft backend scaffold for local testing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import auth, dashboard, loans, members, risk

app = FastAPI(
    title="Ruiru PCEA SACCO Portal API",
    description="Backend API for the Ruiru PCEA SACCO clone portal.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(members)
app.include_router(loans)
app.include_router(dashboard)
app.include_router(risk)


@app.get("/")
def read_root():
    return {"message": "Ruiru PCEA SACCO Portal API is running"}
