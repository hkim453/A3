import random

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import Book, User, Author, Publisher, BooksInventory
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            pass
        return user

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_number_of_books(self) -> int:
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__id == id).one()
        except NoResultFound:
            pass
        return book

    def get_all_book_ids(self):
        book_ids = self._session_cm.session.query(Book).order_by(asc(Book._Book__id)).all()
        return book_ids

    def get_random_book(self) -> Book:
        book = None
        nr_books = self.get_number_of_books()
        if nr_books > 0:
            random_number = random.randint(0, nr_books-1)
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == random_number).one()
        return book

    def get_all_books_alphabetical(self):
        sorted_books = self._session_cm.session.query(Book).order_by(asc(Book._Book__title)).all()
        return sorted_books

    def get_all_books_release_year(self):
        sorted_books = self._session_cm.session.query(Book).order_by(desc(Book._Book__release_year)).all()
        return sorted_books

    def get_all_books_average_rating(self):
        sorted_books = self._session_cm.session.query(Book).order_by(desc(Book._Book__average_rating)).all()
        return sorted_books

    def get_books_by_author(self, author_id: int):
        sorted_books = self._session_cm.session.query(Book).order_by(desc(Book._Book__average_rating)).all()
        return sorted_books













