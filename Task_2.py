from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Book:

    def __init__(self, title: str, author: str, year: int) -> None:
        self.title = title
        self.author = author
        self.year = year

    def __str__(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"


class LibraryInterface(ABC):

    @abstractmethod
    def add_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        pass

    @abstractmethod
    def get_books(self) -> list[Book]:
        pass


class Library(LibraryInterface):

    def __init__(self) -> None:
        self._books: list[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)
        logger.info("Book added: %s", book)

    def remove_book(self, title: str) -> None:
        for book in self._books:
            if book.title == title:
                self._books.remove(book)
                logger.info("Book removed: %s", book)
                return
        logger.warning("Book with title '%s' not found.", title)

    def get_books(self) -> list[Book]:
        return self._books


class LibraryManager:

    def __init__(self, library: LibraryInterface) -> None:
        self.library = library

    def add_book(self, title: str, author: str, year_str: str) -> None:
        try:
            year = int(year_str)
        except ValueError:
            logger.error("Invalid year format. Must be a number.")
            return

        book = Book(title, author, year)
        self.library.add_book(book)

    def remove_book(self, title: str) -> None:
        self.library.remove_book(title)

    def show_books(self) -> None:
        books = self.library.get_books()
        if not books:
            logger.info("Library is empty.")
            return
        for book in books:
            logger.info(book)


def main() -> None:
    library = Library()
    manager = LibraryManager(library)

    while True:
        command = input("Enter command (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                year = input("Enter book year: ").strip()
                manager.add_book(title, author, year)

            case "remove":
                title = input("Enter book title to remove: ").strip()
                manager.remove_book(title)

            case "show":
                manager.show_books()

            case "exit":
                logger.info("Exiting program.")
                break

            case _:
                logger.warning("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
