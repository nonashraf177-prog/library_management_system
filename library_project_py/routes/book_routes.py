from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.services import book_service
from app.core.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.role_dependency import admin_required

# initialize router:
router = APIRouter(prefix="/books", tags=["Books"])

# Create Book (Admin only)
@router.post("/", response_model=BookResponse)
def create_book_route(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book)


# Get All Books
@router.get("/", response_model=list[BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    return book_service.get_books(db, skip, limit, search, category)


# Get Book by ID
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


# Update Book
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book_service.update_book(db, book, data)


# Delete Book (Admin only)
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_service.delete_book(db, book)
    return {"message": "Book deleted"}