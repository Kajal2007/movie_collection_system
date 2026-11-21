# Movie Collection Management System

A simple CRUD web app to manage a personal movie collection.

**Tech stack:** HTML, CSS, Python, Flask, MySQL

**Features:** Add movie, view all movies, update movie, delete movie, search by name.

---

## 1. Folder Structure

```
MovieCollectionSystem/
├── app.py             # Flask app: all routes + CRUD logic
├── database.py        # MySQL connection function
├── database.sql       # Creates database, table and sample data
├── requirements.txt   # Python packages to install
├── README.md          # This file
├── templates/         # HTML pages (Jinja2 templates)
│   ├── base.html      # Common layout (header, messages, footer)
│   ├── index.html     # Home page: list + search + edit/delete buttons
│   ├── add_movie.html # Add movie form
│   └── edit_movie.html# Edit movie form
├── static/
│   ├── css/style.css  # All styling
│   └── images/        # Put your own images here (optional)
└── screenshots/       # Put project screenshots here
```

---

## 2. Database

Database: `movie_collection`  |  Table: `movies`

| Column        | Type          | Meaning                          |
|---------------|---------------|----------------------------------|
| movie_id      | INT, PK, AUTO_INCREMENT | Unique id of the movie |
| movie_name    | VARCHAR(150)  | Name of the movie                |
| genre         | VARCHAR(50)   | Action, Drama, ...               |
| release_year  | INT           | Year of release                  |
| rating        | DECIMAL(3,1)  | 0.0 to 10.0                      |
| language      | VARCHAR(50)   | English, Hindi, ...              |

```sql
CREATE DATABASE IF NOT EXISTS movie_collection;
USE movie_collection;

CREATE TABLE IF NOT EXISTS movies (
    movie_id     INT AUTO_INCREMENT PRIMARY KEY,
    movie_name   VARCHAR(150) NOT NULL,
    genre        VARCHAR(50)  NOT NULL,
    release_year INT          NOT NULL,
    rating       DECIMAL(3,1) NOT NULL,
    language     VARCHAR(50)  NOT NULL
);
```

The full script with sample data is in `database.sql`.

---

## 3. Installation and Setup in VS Code

### Step 1: Install the tools
1. **Python 3.9+**: https://www.python.org/downloads/ (tick "Add Python to PATH" during install).
2. **MySQL Server + MySQL Workbench**: https://dev.mysql.com/downloads/ (remember the root password you set).
3. **VS Code**: https://code.visualstudio.com/ and install the **Python** extension (by Microsoft).

### Step 2: Open the project
1. Extract the project folder `MovieCollectionSystem`.
2. In VS Code: **File > Open Folder** and select `MovieCollectionSystem`.
3. Open the terminal: **Terminal > New Terminal**.

### Step 3: Create a virtual environment (recommended)
```bash
python -m venv venv
```
Activate it:
- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- Windows (CMD): `venv\Scripts\activate.bat`
- macOS / Linux: `source venv/bin/activate`

If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope Process Bypass` once and try again.

### Step 4: Install the packages
```bash
pip install -r requirements.txt
```

### Step 5: Create the database
**Option A: MySQL Workbench**
1. Open Workbench and connect to your local server.
2. **File > Open SQL Script** and choose `database.sql`.
3. Click the lightning bolt (Execute).

**Option B: Command line**
```bash
mysql -u root -p < database.sql
```

### Step 6: Set your MySQL password
Open `database.py` and change:
```python
"password": "your_mysql_password",
```

### Step 7: Run the app
```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser. Press `Ctrl + C` in the terminal to stop.

---

## 4. Explanation of Each File (Simple Language)

### database.sql
Run once. It creates the database, the `movies` table and four sample movies.
`AUTO_INCREMENT` means MySQL gives each new movie the next id automatically, and `PRIMARY KEY` means no two movies can share an id.

### requirements.txt
Lists the packages the project needs: `Flask` (web framework) and `mysql-connector-python` (lets Python talk to MySQL).

### database.py
Holds the connection settings in a dictionary and one function, `get_connection()`.
Every route calls this function when it needs the database, so the settings live in only one place.

### app.py
The brain of the project. Important parts:

| Part | What it does |
|------|--------------|
| `app = Flask(__name__)` | Creates the web application |
| `app.secret_key` | Needed by Flask to show flash messages |
| `GENRES` | List used to build the genre dropdown and to check the chosen genre |
| `validate_movie(form)` | Checks every form field and returns clean data plus a list of error messages |
| `@app.route("/")` `index()` | **Read + Search.** Runs `SELECT`. If `?search=` is present, uses `WHERE movie_name LIKE` |
| `@app.route("/add")` `add_movie()` | **Create.** GET shows the empty form, POST validates and runs `INSERT` |
| `@app.route("/edit/<id>")` `edit_movie()` | **Update.** GET loads the movie into the form, POST validates and runs `UPDATE` |
| `@app.route("/delete/<id>")` `delete_movie()` | **Delete.** Runs `DELETE`. Accepts POST only |
| `try / except` | Catches database errors and shows a message instead of crashing |
| `conn.commit()` | Saves INSERT / UPDATE / DELETE permanently |
| `%s` placeholders | Pass values safely to SQL (prevents SQL injection) |

Typical request flow: browser asks for a URL, Flask finds the matching route, the function talks to MySQL, then `render_template()` sends back an HTML page.

### templates/base.html
The shared layout. Other pages use `{% extends "base.html" %}` and fill in `{% block content %}`, so the header and footer are written only once. It also displays flash messages.

### templates/index.html
Home page. Has the search box, a table made with a Jinja `{% for %}` loop, and Edit / Delete buttons. Delete is a small form using POST with a confirmation popup. Shows a friendly message when the list is empty or the search finds nothing.

### templates/add_movie.html
The add form. If validation fails, the values the user typed are put back into the fields so they do not retype everything.

### templates/edit_movie.html
Same form, pre-filled with the existing movie data. The genre dropdown selects the saved genre.

### static/css/style.css
All the styling: colours (in `:root` variables), top bar, table, buttons, forms and alert messages. The `@media (max-width: 700px)` block turns the table into stacked cards on phones, which makes the site responsive.

---

## 5. Test Checklist
1. Open the home page: 4 sample movies appear.
2. Add a movie: it appears at the top.
3. Try to add a movie with an empty name or rating `15`: an error message appears.
4. Edit a movie and save: the changes show in the list.
5. Search `dark`: only matching movies show.
6. Delete a movie: confirm the popup and it disappears.

## 6. Common Errors

| Error | Fix |
|-------|-----|
| `Access denied for user 'root'` | Wrong password in `database.py` |
| `Unknown database 'movie_collection'` | Run `database.sql` first |
| `ModuleNotFoundError: flask` | Activate the venv and run `pip install -r requirements.txt` |
| `Can't connect to MySQL server` | Start the MySQL service |
| Port 5000 already in use | Change to `app.run(debug=True, port=5001)` |

---

## 7. Interview Questions and Answers

**Q1. What is Flask?**
A lightweight Python web framework. It handles URLs (routes), requests and responses, and renders HTML templates.

**Q2. What is a route?**
A URL mapped to a Python function using `@app.route()`. For example, `/add` runs `add_movie()`.

**Q3. What are GET and POST?**
GET asks the server for a page (open a form, view data). POST sends data to the server (submit a form). Add, edit and delete use POST to change data.

**Q4. What is CRUD? Where is it in your project?**
Create, Read, Update, Delete. Create is `add_movie`, Read is `index`, Update is `edit_movie`, Delete is `delete_movie`. They use `INSERT`, `SELECT`, `UPDATE`, `DELETE`.

**Q5. How does Flask connect to MySQL?**
Using `mysql-connector-python`. `mysql.connector.connect()` opens a connection, `cursor.execute()` runs SQL, `commit()` saves changes, and I close the cursor and connection afterwards.

**Q6. Why do you use `%s` instead of putting values directly into the query?**
To prevent SQL injection. The driver sends values separately from the SQL, so user input is never treated as SQL code.

**Q7. Why call `conn.commit()`?**
INSERT, UPDATE and DELETE only become permanent after commit. SELECT does not need it.

**Q8. What is a primary key?**
A column that uniquely identifies each row. `movie_id` is the primary key; it cannot repeat or be NULL.

**Q9. What is Jinja2?**
Flask's template engine. It lets HTML use `{{ variable }}`, `{% for %}`, `{% if %}`, and `{% extends %}` for reusable layouts.

**Q10. Why use `base.html`?**
Template inheritance. The header, footer and CSS link are written once and reused, so changes are made in one place.

**Q11. What does `flash()` do?**
Stores a one-time message (like "Movie added") that is shown on the next page, then disappears.

**Q12. How does search work?**
The search form sends `?search=text` using GET. The route reads it with `request.args.get()` and runs `WHERE movie_name LIKE '%text%'`.

**Q13. How did you validate the input?**
`validate_movie()` checks that fields are not empty, year and rating are numbers, rating is between 0 and 10, and the year is realistic. If anything is wrong, error messages are shown and nothing is saved. HTML attributes like `required` and `min/max` add a first check in the browser.

**Q14. Why is delete done with POST and not a link?**
A link (GET) can be triggered by accident, by browsers pre-loading pages, or by crawlers. POST with a confirmation is safer.

**Q15. What does `redirect(url_for("index"))` do?**
After saving, it sends the user to the home page. This also stops the form from being re-submitted if the page is refreshed.

**Q16. What is `debug=True`?**
Development mode: the server restarts automatically after code changes and shows detailed errors. It must be turned off in production.

**Q17. What is `cursor(dictionary=True)`?**
Rows come back as dictionaries, so templates can use `movie.movie_name` instead of index numbers like `row[1]`.

**Q18. How is the site responsive?**
CSS flexbox and grid, a viewport meta tag, and a media query that converts the table rows into stacked cards on small screens.

**Q19. What is the difference between `VARCHAR` and `DECIMAL(3,1)`?**
`VARCHAR` stores text. `DECIMAL(3,1)` stores numbers with up to 3 digits, 1 after the decimal point (0.0 to 99.9), which suits ratings.

**Q20. What improvements would you add next?**
Pagination, sorting, a movie poster upload, duplicate-name check, environment variables for the password, and a CSRF protection library.

---

## 8. Possible Extensions (Beginner Friendly)
- Sort by rating or year
- Filter by genre
- Add a poster image per movie
- Move DB password to a `.env` file
