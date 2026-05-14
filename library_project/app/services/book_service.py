# app/services/book_service.py
from sqlalchemy.orm import Session
from app.models.book_model import Book
from app.core.redis_client import cache_get, cache_set, cache_delete

CACHE_TTL = 60  # seconds


# ── Create ───────────────────────────────────────────────────────────────────

def create_book(db: Session, book_data):
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    cache_delete("books:all")                    # invalidate list cache
    return book


# ── Read all ─────────────────────────────────────────────────────────────────

def get_books(db: Session, skip: int = 0, limit: int = 10,
              search: str = None, category: str = None):
    # Only cache the plain, unfiltered first page
    use_cache = (skip == 0 and not search and not category)
    cache_key = "books:all"

    if use_cache:
        cached = cache_get(cache_key)
        if cached is not None:
            return cached            # return raw list (dicts); FastAPI serialises it

    query = db.query(Book)
    if search:
        query = query.filter(Book.title.contains(search))
    if category:
        query = query.filter(Book.category == category)

    results = query.offset(skip).limit(limit).all()

    if use_cache:
        # Serialise SQLAlchemy objects to dicts before caching
        serialised = [
            {c.name: getattr(b, c.name) for c in b.__table__.columns}
            for b in results
        ]
        cache_set(cache_key, serialised, ex=CACHE_TTL)
        return results               # return ORM objects for response_model

    return results


# ── Read one ─────────────────────────────────────────────────────────────────

def get_book(db: Session, book_id: int):
    cache_key = f"book:{book_id}"
    cached = cache_get(cache_key)
    if cached is not None:
        # Re-fetch ORM object so response_model works correctly
        return db.query(Book).filter(Book.id == book_id).first()

    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        serialised = {c.name: getattr(book, c.name) for c in book.__table__.columns}
        cache_set(cache_key, serialised, ex=CACHE_TTL)
    return book


# ── Update ───────────────────────────────────────────────────────────────────

def update_book(db: Session, book: Book, update_data):
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    cache_delete(f"book:{book.id}")
    cache_delete("books:all")
    return book


# ── Delete ───────────────────────────────────────────────────────────────────

def delete_book(db: Session, book: Book):
    cache_delete(f"book:{book.id}")
    cache_delete("books:all")
    db.delete(book)
    db.commit()
