from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
numbers="0123456789"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)
db.init_app(app)
# db = sqlite3.connect('book-collection.db', check_same_thread=False)
# cursor = db.cursor()
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, nullable=False)

# cursor.execute("CREATE TABLE books (id INT PRIMARY KEY, title VARCHAR(250) NOT NULL UNIQUE, author VARCHAR(250) NOT NULL, rating FLOAT NOT NULL)")
all_books = []

with app.app_context():
    db.create_all()
@app.route('/',methods=['GET','POST'])
def home():
    all_books.clear()
    book_count = len(Books.query.all())
    for i in Books.query.all():
        detail = {'title': i.title, 'author': i.author,
                  'rating': i.rating, 'id':i.id}
        all_books.append(detail)
    if request.method == "POST" and 'add' in request.form:
        all_books.clear()
        with app.app_context():
            row = Books(id=book_count+1, title=request.form['book'], author=request.form['author'], rating=request.form['rating'])
            db.session.add(row)
            db.session.commit()
            for i in Books.query.all():
                detail = {'title': i.title, 'author': i.author,
                          'rating': i.rating, 'id': i.id}
                all_books.append(detail)


        # cursor.execute(f"INSERT INTO books VALUES(1,'ab','bc',7.8)")
        # db.commit()
        book_detail = {'title':request.form['book'], 'author':request.form['author'], 'rating':request.form['rating'], 'id':request.form['id'] }
        all_books.append(book_detail)

    return render_template('index.html',books=all_books, count=book_count)


@app.route("/add")
def add():
    return render_template('add.html')

@app.route('/edit', methods=['GET','POST'])
def edit():
    id = request.args['num']
    book = Books.query.get(id)
    if request.method == "POST":
        arg = ''
        for i in request.query_string.decode():
            if i in numbers:
                arg += i
        arg = int(arg)
        book = Books.query.get(arg)
        book.rating = request.form['newr']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',i=id,j=book)

@app.route('/delete')
def delete():
    id = request.args.get('num')
    book = Books.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

