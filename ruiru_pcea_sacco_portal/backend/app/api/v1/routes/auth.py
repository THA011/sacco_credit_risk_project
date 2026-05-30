from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
def login():
    # Placeholder auth endpoint for the first version.
    return {"access_token": "demo-token", "token_type": "bearer"}
