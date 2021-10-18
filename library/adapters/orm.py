from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym
from library.domain import model

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('pages_read', Integer, nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(4096), nullable=False),
    Column('release_year', String(255), nullable=False),
    Column('ebook', String(255), nullable=False),
    Column('num_pages', String(255), nullable=False),
    Column('url', String(255), nullable=False),
    Column('image_url', String(255), nullable=False),
    Column('average_rating', String(255), nullable=False)
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__pages_read': users_table.c.pages_read
    })

    """mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__read_books': relationship(model.Book),
        '_User__reviews': relationship(model.Review),
        '_User__pages_read': users_table.c.pages_read
    })"""

    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__url': books_table.c.url,
        '_Book__image_url': books_table.c.image_url,
        '_Book__average_rating': books_table.c.average_rating
    })

    """mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__publisher': relationship(model.Publisher),
        '_Book__authors': relationship(model.Author),
        '_Book__release_year': books_table.c.release_year,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__url': books_table.c.url,
        '_Book__image_url': books_table.c.image_url,
        '_Book__average_rating': books_table.c.average_rating
    })"""