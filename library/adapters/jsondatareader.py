import json

from library.domain.model import Publisher, Author, Book

class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__dataset_of_books = []

    @property
    def dataset_of_books(self) -> list:
        return self.__dataset_of_books

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name) as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name) as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json


    def read_json_files(self):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()

        for book_json in books_json:
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            book_instance.publisher = Publisher(book_json['publisher'])
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])

            if book_json['url'] != "":
                book_instance.url = book_json['url']

            if book_json['image_url'] != "":
                book_instance.image_url = book_json['image_url']

            book_instance.average_rating = float(book_json['average_rating'])

            # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_id in list_of_authors_ids:

                numerical_id = int(author_id['author_id'])
                author_name = ""
                for author_json in authors_json:
                    if int(author_json['author_id']) == numerical_id:
                        author_name = author_json['name']

                book_instance.add_author(Author(numerical_id, author_name))


            self.__dataset_of_books.append(book_instance)
