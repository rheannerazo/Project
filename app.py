from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random
import secrets

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pictures.db"
app.config["SECRET_KEY"] = secrets.token_hex(16)
db = SQLAlchemy(app)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=True)


@app.route("/", methods=["GET", "POST"])
def index():
    # Check if the session contains information about the current picture
    if "current_picture" not in session or "guessed" not in session:
        # If not, fetch a new random picture
        session["current_picture"] = fetch_random_picture().id
        session["guessed"] = False

    # Retrieve the current picture based on the session information
    current_picture_id = session["current_picture"]
    current_picture = Picture.query.get(current_picture_id)
    # Initialize guess_result to None
    guess_result = None

    # Check if the form has been submitted and the picture has not been guessed
    if request.method == "POST" and not session["guessed"]:
        guessed_year = request.form.get("guessed_year")

        if guessed_year.isdigit():
            guessed_year = int(guessed_year)
            if guessed_year == current_picture.year:
                guess_result = "Congratulations! You guessed it right!"
            else:
                guess_result = (
                    f"Sorry, the correct year is {current_picture.year}. Try again!"
                )
            session["guessed"] = True

    return render_template(
        "index.html", current_picture=current_picture, guess_result=guess_result
    )


# Clear the session when the user wants to guess the next picture
@app.route("/next_picture", methods=["GET"])
def next_picture():
    # Reset the guessed flag and update the session with a new random picture ID
    session["guessed"] = False
    session["current_picture"] = fetch_random_picture().id
    return redirect(url_for("index"))


def fetch_random_picture():
    return Picture.query.order_by(func.random()).first()
    # random_picture = Picture.query.order_by(func.random()).first()
    # return {'id': random_picture.id, 'url': random_picture.url, 'year': random_picture.year}


@app.route("/add_picture", methods=["GET", "POST"])
def add_picture():
    if request.method == "POST":
        url = request.form.get("url")
        year = request.form.get("year")
        title = request.form.get("title")

        if url and year.isdigit():
            year = int(year)
            new_picture = Picture(url=url, year=year, title=title)
            db.session.add(new_picture)
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("add_picture.html")


if __name__ == "__main__":
    with app.app_context():
        # Create tables if not exists
        db.create_all()
    app.run(debug=True)
