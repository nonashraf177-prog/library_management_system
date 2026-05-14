from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import user_service
from app.schemas.user_schema import UserResponse
from app.dependencies.role_dependency import admin_required

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), _=Depends(admin_required)):
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_required)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}/role", response_model=UserResponse)
def update_role(user_id: int, new_role: str, db: Session = Depends(get_db), _=Depends(admin_required)):
    return user_service.update_user_role(db, user_id, new_role)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_required)):
    return user_service.delete_user(db, user_id)
