from fastapi import APIRouter, HTTPException, status
from app.database import SessionDep
from app.schemas.books import SBook, SBookAdd
from app.repository import BookRepository

router = APIRouter(
    prefix="/books",
    tags=["книги"]
)

@router.post("/", response_model=SBook, status_code=status.HTTP_201_CREATED)
def create_book(book_data: SBookAdd, db: SessionDep):
    repo = BookRepository(db)
    return repo.add_book(book_data)

@router.get("/", response_model=list[SBook])
def get_all(db: SessionDep):
    repo = BookRepository(db)
    return repo.get_all()

@router.get("/{book_id}", response_model=SBook)
def get_book(book_id: int, db: SessionDep):
    repo = BookRepository(db)
    book = repo.get_book(book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )
    
    return book

@router.put("/{book_id}", response_model=SBook)
def update_book(book_id: int, book_data: SBookAdd, db: SessionDep):
    repo = BookRepository(db)

    new_book = repo.update_book(book_id, book_data)

    if new_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return new_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: SessionDep):
    repo = BookRepository(db)
    success = repo.delete_book(book_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return None