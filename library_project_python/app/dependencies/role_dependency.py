#role depenency

from fastapi import Depends, HTTPException, status
from app.models.user_model import User
from .auth_dependency import get_current_user 

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Forbidden: Admin access only"
        )
    return current_user