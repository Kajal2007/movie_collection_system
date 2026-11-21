"""
app.py
------
Main Flask application for the Movie Collection Management System.
Contains all routes (URLs) and the CRUD logic:
    Create -> add_movie()
    Read   -> index()  (also handles search)
    Update -> edit_movie()
    Delete -> delete_movie()
"""

from datetime import date

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for

from database import get_connection

app = Flask(__name__)
app.secret_key = "change-this-secret-key"   # needed for flash() messages

# Genres shown in the dropdown list of the forms
GENRES = ["Action", "Comedy", "Drama", "Horror", "Romance",
          "Sci-Fi", "Thriller", "Animation", "Documentary", "Other"]


# ---------------------------------------------------------------
# Helper function: validate the form data
# ---------------------------------------------------------------
def validate_movie(form):
    """
    Check the form values.
    Returns (data, errors):
        data   -> cleaned values (a dictionary)
        errors -> list of error messages (empty list means all OK)
    """
    errors = []

    name = form.get("movie_name", "").strip()
    genre = form.get("genre", "").strip()
    language = form.get("language", "").strip()
    year_text = form.get("release_year", "").strip()
    rating_text = form.get("rating", "").strip()

    # Text fields must not be empty
    if not name:
        errors.append("Movie name is required.")
    if genre not in GENRES:
        errors.append("Please choose a genre.")
    if not language:
        errors.append("Language is required.")

    # Release year must be a number in a sensible range
    year = None
    try:
        year = int(year_text)
        if year < 1888 or year > date.today().year + 5:
            errors.append("Release year must be between 1888 and "
                          f"{date.today().year + 5}.")
    except ValueError:
        errors.append("Release year must be a number.")

    # Rating must be a number from 0 to 10
    rating = None
    try:
        rating = float(rating_text)
        if rating < 0 or rating > 10:
            errors.append("Rating must be between 0 and 10.")
    except ValueError:
        errors.append("Rating must be a number.")

    data = {"name": name, "genre": genre, "year": year,
            "rating": rating, "language": language}
    return data, errors


# ---------------------------------------------------------------
# READ + SEARCH: show all movies (or only the ones that match)
# ---------------------------------------------------------------
@app.route("/")
def index():
    search = request.args.get("search", "").strip()   # text typed in search box
    movies = []

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)   # rows come back as dictionaries

        if search:
            # LIKE with % finds names that CONTAIN the search text
            cursor.execute(
                "SELECT * FROM movies WHERE movie_name LIKE %s ORDER BY movie_id DESC",
                ("%" + search + "%",),
            )
        else:
            cursor.execute("SELECT * FROM movies ORDER BY movie_id DESC")

        movies = cursor.fetchall()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "error")

    return render_template("index.html", movies=movies, search=search)


# ---------------------------------------------------------------
# CREATE: add a new movie
# ---------------------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        data, errors = validate_movie(request.form)

        if errors:
            for e in errors:
                flash(e, "error")
            # Show the form again with the values the user already typed
            return render_template("add_movie.html", genres=GENRES, form=request.form)

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # %s placeholders protect against SQL injection
            cursor.execute(
                "INSERT INTO movies (movie_name, genre, release_year, rating, language) "
                "VALUES (%s, %s, %s, %s, %s)",
                (data["name"], data["genre"], data["year"], data["rating"], data["language"]),
            )
            conn.commit()      # save the change permanently
            cursor.close()
            conn.close()
            flash("Movie added successfully.", "success")
            return redirect(url_for("index"))
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")
            return render_template("add_movie.html", genres=GENRES, form=request.form)

    # GET request: just show an empty form
    return render_template("add_movie.html", genres=GENRES, form={})


# ---------------------------------------------------------------
# UPDATE: edit an existing movie
# ---------------------------------------------------------------
@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == "POST":
            data, errors = validate_movie(request.form)

            if errors:
                for e in errors:
                    flash(e, "error")
                movie = {"movie_id": movie_id, "movie_name": data["name"],
                         "genre": data["genre"], "release_year": request.form.get("release_year"),
                         "rating": request.form.get("rating"), "language": data["language"]}
                cursor.close()
                conn.close()
                return render_template("edit_movie.html", movie=movie, genres=GENRES)

            cursor.execute(
                "UPDATE movies SET movie_name=%s, genre=%s, release_year=%s, "
                "rating=%s, language=%s WHERE movie_id=%s",
                (data["name"], data["genre"], data["year"], data["rating"],
                 data["language"], movie_id),
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash("Movie updated successfully.", "success")
            return redirect(url_for("index"))

        # GET request: load the current movie details into the form
        cursor.execute("SELECT * FROM movies WHERE movie_id = %s", (movie_id,))
        movie = cursor.fetchone()
        cursor.close()
        conn.close()

        if movie is None:
            flash("Movie not found.", "error")
            return redirect(url_for("index"))

        return render_template("edit_movie.html", movie=movie, genres=GENRES)

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "error")
        return redirect(url_for("index"))


# ---------------------------------------------------------------
# DELETE: remove a movie (POST only, so a link can't delete by accident)
# ---------------------------------------------------------------
@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE movie_id = %s", (movie_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Movie deleted.", "success")
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "error")
    return redirect(url_for("index"))


# Run the app (debug=True restarts the server on code changes)
if __name__ == "__main__":
    app.run(debug=True)
