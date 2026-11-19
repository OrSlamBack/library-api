from pydantic import BaseModel, Field, ConfigDict

class SBookAdd(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="Название книги")
    author: str = Field(min_length=1, max_length=100, description="Имя автора")
    year: int = Field(ge=-99999, le=99999, description="Год издания")
    pages: int = Field(ge=11, le=9999, description="Количество страниц")
    is_read: bool = False

class SBook(SBookAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)