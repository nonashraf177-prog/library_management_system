from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.borrow_service import borrow_book, return_book, get_user_borrows
from app.dependencies.auth_dependency import get_current_user
from app.schemas.borrow_schema import BorrowResponse

router = APIRouter(prefix="/borrow", tags=["Borrow"])


@router.post("/{book_id}", response_model=BorrowResponse)
def borrow(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return borrow_book(db, user.id, book_id)


@router.post("/return/{book_id}")
def return_api(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return return_book(db, user.id, book_id)


@router.get("/my-books", response_model=list[BorrowResponse])
def my_books(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_user_borrows(db, user.id)
