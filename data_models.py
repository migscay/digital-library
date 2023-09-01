from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column("author_id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(250), nullable=False)
    birth_date = db.Column("birth_date", db.String(10), nullable=True)
    date_of_death = db.Column("date_of_death", db.String(10), nullable=True)

    def __str__(self):
        return f"Author(id = {self.author_id}, name = {self.name}, Date of Birth = {self.birth_date}, " \
               f"Date of Death = {self.date_of_death})"


class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column("book_id", db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    isbn = db.Column("isbn", db.Integer, unique=True, nullable=False)
    title = db.Column("title", db.String(250), nullable=False)
    publication_year = db.Column("publication_year", db.Integer)

    def __str__(self):
        return f"Book(id = {self.book_id}, author = {self.author_id}, isbn = {self.isbn}, " \
               f"title = {self.title}, publication year = {self.publication_year})"

