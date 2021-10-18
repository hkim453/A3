from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.data_importer import load_users
from library.adapters.jsondatareader import BooksJSONReader

def populate(data_path: Path, repo: AbstractRepository):
    users = load_users(data_path, repo)

    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'

    path_to_books_file = str(data_path / books_file_name)
    path_to_authors_file = str(data_path / authors_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file)
    reader.read_json_files()

    for book in reader.dataset_of_books:
        repo.add_book(book)