from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
import os

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"/data/library.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

db.init_app(app)


@app.route('/', methods=["GET", "POST"])
def home():
    # check if there are books
    book = db.session.query(Book).first()
    if book:
        searchable = True
    else:
        searchable = False

    if request.method == "POST":
        title = request.form['title']
        # search books by title
        books_authors = db.session.query(Book.book_id, Book.isbn, Book.title, Author.name).join(Author) \
            .order_by(Book.title.asc()).filter(Book.title.ilike(r"%{}%".format(title))).all()
        return render_template('home.html', books_authors=books_authors, searchable=searchable, search_term=title)

    sorting = request.args.get('sorting', 'book_title')
    if sorting == "book_title":
        books_authors = db.session.query(Book.book_id, Book.isbn, Book.title, Author.name).join(Author)\
            .order_by(Book.title.asc()).all()
    else:
        books_authors = db.session.query(Book.book_id, Book.isbn, Book.title, Author.name).join(Author)\
            .order_by(Author.name.asc()).all()

    return render_template('home.html', books_authors=books_authors, sorting=sorting, searchable=searchable)


@app.route('/add_author', methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        # Create an instance of the Author table class
        author = Author(
            name=request.form['name'],
            birth_date=request.form['birthdate'],
            date_of_death=request.form['date_of_death']
        )
        db.session.add(author)
        db.session.commit()

        message = f"New Author Added {author.__str__()}"

        return render_template('add_author.html', message=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=["GET", "POST"])
def add_book():
    # get authors
    authors = db.session.query(Author). \
        order_by(Author.name.asc()). \
        all()

    if request.method == "POST":
        # Create an instance of the Book table class
        book = Book(
            author_id=request.form['author_id'],
            isbn=request.form['isbn'],
            title=request.form['title'],
            publication_year=request.form['publication_year']
        )
        print(f"after Posting {request.form}")
        db.session.add(book)
        db.session.commit()

        message = f"New Book Added  {book.__str__()}"
        return render_template('add_book.html', authors=authors, message=message)

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=["GET", "POST"])
def delete_book(book_id):
    if request.method == "POST":
        # Delete book by book_id
        db.session.query(Book).filter(Book.book_id == book_id).delete()
        db.session.commit()
        return redirect(url_for('home'))

    # search books by book_id
    book = db.session.query(Book.book_id, Book.isbn, Book.title, Author.name).join(Author) \
        .filter(Book.book_id == book_id).one()

    return render_template('delete-book.html', book=book)


if __name__ == '__main__':
    app.run(debug=True)
