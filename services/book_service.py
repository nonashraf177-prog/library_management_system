from sqlalchemy.orm import Session
from app.models.book_model import Book

# Create Book
def create_book(db, book_data):
    book = Book(**book_data.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


# Get All Books (with pagination + filtering + search)
def get_books(db, skip=0, limit=10, search=None, category=None):
    query = db.query(Book)

    if search:
        query = query.filter(Book.title.contains(search))

    if category:
        query = query.filter(Book.category == category)

    return query.offset(skip).limit(limit).all()


# Get Book by ID
def get_book(db, book_id):
    return db.query(Book).filter(Book.id == book_id).first()


# Update Book
def update_book(db, book, update_data):
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


# Delete Book
def delete_book(db, book):
    db.delete(book)
    db.commit()