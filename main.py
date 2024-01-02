from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my-books-collection.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
db = SQLAlchemy(app)


class My_book_collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)


db.create_all()

class Bookform(FlaskForm):
    bookname = StringField('Bookname', validators=[DataRequired()])
    author=StringField('Author', validators=[DataRequired()])
    rating = SelectField('Book rating', validators=[DataRequired()], choices=["x", "xx","xxx","xxxx","xxxxx"])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    all_books = db.session.query(My_book_collection).all()
    return render_template("index.html", all_books=all_books)


@app.route('/add', methods=["GET", "POST"])
def add():
    form = Bookform()
    if form.validate_on_submit():
        new_book = My_book_collection(title=f"{form.bookname.data}", author=f"{form.author.data}",
                                      rating=f"{form.rating.data}")
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    # непонятно
    return render_template("add.html", form=form)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        item_id = request.form["ititle"]
        book_update = My_book_collection.query.get(item_id)
        book_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    item_id = request.args.get('id')
    book_selected = My_book_collection.query.get(item_id)
    return render_template("editratings.html", book=book_selected)


@app.route('/d')
def de():
    item_id = request.args.get("id")
    book_to_delete=My_book_collection.query.get(item_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
