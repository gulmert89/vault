from datetime import date
from typing import Optional
from starlette import status
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, Path, HTTPException  # , Body


app = FastAPI()
current_year = date.today().year


class Book:
    book_id: str
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(
            self,
            book_id,
            title,
            author,
            description,
            rating,
            published_date
    ) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    book_id: Optional[int | None] = Field(
        gt=0,
        title="Book ID",
        description="Book ID is assigned incrementally in the background."
    )
    title: str = Field(max_length=100)
    author: str = Field(max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0, lt=(1+current_year))

    class Config:  # A Pydantic class
        schema_extra = {
            "example": {
                "title": "A New Default Book",
                "author": "Mr.Nobody",
                "description": "This description does not exist.",
                "rating": 5,
                "published_date": 1989
            }
        }


book_list = [
    Book(1, "Nice Booktitle1", "Mr.Author1", "Super Desc1", 5, 2012),
    Book(2, "Some Booktitle2", "Lil Author2", "Uber Desc2", 4, 1999),
    Book(3, "About Booktitle3", "Smol Author3", "Grand Desc3", 3, 2021),
    Book(4, "Not a Booktitle4", "Boi Author4", "Huge Desc4", 2, 2023)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books() -> list:
    return book_list


@app.get("/get_book/by_id/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_from_id(book_id: int = Path(gt=0)):  #  CANT DO THIS -> Book | str
    for book in book_list:
        if book.book_id == book_id:
            return book
    no_book = "The book with ID number {} does not exist."
    raise HTTPException(status_code=404, detail=no_book.format(book_id))


@app.get("/get_book/by_rating", status_code=status.HTTP_200_OK)
async def read_book_from_rating(book_rating: int = Query(gt=0, lt=6)) -> list:
    requested_list = []
    for book in book_list:
        if book.rating == book_rating:
            requested_list.append(book)
    return requested_list


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest) -> None:
    new_book = Book(**book_request.dict())
    book_list.append(assign_book_id(new_book))


def assign_book_id(book: Book) -> Book:
    book.book_id = 1 if len(book_list) == 0 else book_list[-1].book_id + 1  # ternary operator
    return book


@app.delete("/delete_books/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Query(gt=0)) -> None:
    for i, book in enumerate(book_list):
        if book_id == book.book_id:
            book_list.pop(i)
            break
    else:
        no_book = "The book with ID number {} does not exist."
        raise HTTPException(
            status_code=404,
            detail=no_book.format(book_id)
        )


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest) -> None:
    for i in range(len(book_list)):
        if book.book_id == book_list[i].book_id:
            book_list[i] = book
            break
    else:
        no_book = "The book with ID number {} does not exist."
        raise HTTPException(
            status_code=404,
            detail=no_book.format(book.book_id)
        )


# Assignment
@app.get("/get_book/by_published_date", status_code=status.HTTP_200_OK)
async def read_book_from_published_date(
    publish_date: int = Query(gt=0, lt=(1+current_year))
) -> list:
    requested_list = []
    for book in book_list:
        if book.published_date == publish_date:
            requested_list.append(book)
    return requested_list
