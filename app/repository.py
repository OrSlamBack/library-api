from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from app.models.books import Book
from app.schemas.books import SBook, SBookAdd

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Book]: 
        statement = select(Book)
        return self.db.scalars(statement).all()

    def get_book(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def add_book(self, book_data: SBookAdd) -> Book:
        book = Book(**(book_data.model_dump()))
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update_book(self, book_id: int, book_data: SBookAdd) -> Book | None:
        statement = (
            update(Book)
            .where(Book.id == book_id)
            .values(**(book_data.model_dump()))
        )
        result = self.db.execute(statement)
        self.db.commit()

        if result.rowcount == 0:
            return None # книга не найдена, потому что 0 изменений

        return self.get_book(book_id)

    def delete_book(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        if book is None:
            return False

        self.db.delete(book)
        self.db.commit()
        return True