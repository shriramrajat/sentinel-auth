from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def admin_hello():
    return {"message": "Admin area"}
