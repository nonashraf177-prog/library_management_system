from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.borrow_model import BorrowRecord
from app.models.book_model import Book
import datetime

MAX_BOOKS_PER_USER = 3

def borrow_book(db: Session, user_id: int, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.available:
        raise HTTPException(status_code=400, detail="Book not available")

    count = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.status == "borrowed"
    ).count()

    if count >= MAX_BOOKS_PER_USER:
        raise HTTPException(status_code=400, detail="Borrow limit reached (max 3 books)")

    existing = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.status == "borrowed"
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You already borrowed this book")

    borrow = BorrowRecord(user_id=user_id, book_id=book_id)
    book.available = False  # Mark as unavailable

    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    return borrow


def return_book(db: Session, user_id: int, book_id: int):
    record = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.status == "borrowed"
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="No active borrow record found")

    book = db.query(Book).filter(Book.id == book_id).first()

    record.status = "returned"
    record.return_date = datetime.datetime.utcnow()

    if book:
        book.available = True  # Mark as available again

    db.commit()

    return {"message": "Book returned successfully"}


def get_user_borrows(db: Session, user_id: int):
    return db.query(BorrowRecord).filter(BorrowRecord.user_id == user_id).all()
