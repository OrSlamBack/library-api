from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import engine, Base
from app.routers.books import router as books_router

from app.models.books import Book  


@asynccontextmanager
async def lifespan(app: FastAPI):
    #ЗАПУСК сервера
    Base.metadata.create_all(bind=engine)
    yield
    #ОСТАНОВКА сервера


app = FastAPI(
    title="MyLibrary API",
    description="API для управления домашней библиотекой",
    version="1.0.0",
    lifespan=lifespan,
)

# Подключаем роутер с эндпоинтами для книг
app.include_router(books_router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "Добро пожаловать в MyLibrary API!"}