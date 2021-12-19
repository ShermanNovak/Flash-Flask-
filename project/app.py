import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///flash.db")

@app.route("/")
def index():
    return render_template("welcome.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""

    # When requested via GET. should display registration form
    if request.method == "GET":
        return render_template("signup.html")

    # Be sure to check for invalid inputs
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # render an apology if the username is blank
        if not username:
            return apology("must provide username")

        # render an apology if the password is blank
        elif not password or not confirmation:
            return apology("must provide password")

        elif password != confirmation:
            return apology("passwords do not match")

        elif len(password) < 8 or len(username) < 8:
            return apology("passwords must be at least 8 characters long")

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # render an apology if the username already exists
        if len(user) != 0:
            return apology("username already exists")

    # When form is submitted via POST, insert the new user into users table and hash the user's password
        user_id = db.execute("INSERT INTO users(username, hash) VALUES(?,?)", username, generate_password_hash(password))
        flash('Successfully registered.')

        session["user_id"] = user_id
        return redirect("/home")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        elif not password:
            return apology("must provide password")

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = user[0]["user_id"]

        # Redirect user to home page
        return redirect("/home")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route('/home')
@login_required
def home():
    # Query for a list of decks the user has
    decks = db.execute('SELECT * FROM decks WHERE user_id = ?', session['user_id'])

    username = db.execute('SELECT username FROM users WHERE user_id = ?', session['user_id'])
    return render_template('home.html', decks=decks, username=username)


@app.route('/delete/<deck_name>', methods=['POST'])
def delete_deck(deck_name):

    # Delete cards from database first (foreign key constraint)
    db.execute('DELETE FROM cards WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
    # Delete deck from database
    db.execute('DELETE FROM decks WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
    flash('Successfully deleted ' + deck_name + '.')
    return redirect('/home')


@app.route('/createdeck', methods=["GET", "POST"])
@login_required
def createdeck():
    if request.method == "GET":
        return render_template('createdeck.html')
    else:
        deck_name = request.form.get('deck_name')
        if not deck_name:
            return apology('Deck name required')

        # Check if the deck name already exists
        current_decks = db.execute('SELECT deck_name FROM decks WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
        if len(current_decks) != 0:
            return apology('Deck already exists')

        # Create deck in database in the decks table
        db.execute("INSERT INTO decks(user_id, deck_name, deck_size, timing) VALUES(?,?,?, datetime('now', 'localtime'))", session['user_id'], deck_name, 0)
        flash('Successfully created ' + deck_name + '.')
        return redirect('/create')


@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        # Query for a list of decks the user has
        decks = db.execute('SELECT deck_name FROM decks WHERE user_id = ?', session['user_id'])
        return render_template('create.html', decks=decks)
    else:
        deck_name = request.form.get('deck_name')
        front = request.form.get('front')
        back = request.form.get('back')
        if not deck_name:
            return apology('Deck name required')
        if not front:
            return apology('Title of card required')
        if not back:
            return apology('Content of card required')

        # Update deck_size with each card made
        deck_size = db.execute('SELECT deck_size FROM decks WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
        deck_size = int(deck_size[0]['deck_size']) + 1
        db.execute('UPDATE decks SET deck_size = ? WHERE user_id = ? AND deck_name = ?', deck_size, session['user_id'], deck_name)

        # Insert card into database using deck_id
        deck_id = db.execute('SELECT deck_id FROM decks WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
        if not deck_id:
            return apology('Cannot get deck_id')

        db.execute('INSERT INTO cards(user_id, deck_name, deck_id, card_id, title, content) VALUES(?,?,?,?,?,?)', session['user_id'], deck_name, int(deck_id[0]['deck_id']), deck_size, front, back)
        flash('Successfully created card')
        return redirect('/create')


@app.route('/view/<deck_name>/<int:card_id>', methods=["GET", "POST"])
@login_required
def viewer(deck_name, card_id):
    if request.method == "GET":
        # Query for card title and content
        card = db.execute('SELECT title, content FROM cards WHERE user_id = ? AND deck_name = ? AND card_id = ?', session['user_id'], deck_name, card_id)
        if not card:
            return apology('No card found')

        deck_size = db.execute('SELECT deck_size FROM decks WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
        deck_size = int(deck_size[0]['deck_size'])
        return render_template('viewer.html', card=card, deck_name=deck_name, card_id=card_id, deck_size=deck_size)

    else:
        # Update status of card
        status = request.form['status']
        if not status:
            return apology('Please indicate card status.')
        db.execute('UPDATE cards SET status = ? WHERE user_id = ? AND deck_name = ? AND card_id = ?', status, session['user_id'], deck_name, card_id)

        # Get deck_size == last_card
        deck_size = db.execute('SELECT deck_size FROM decks WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
        deck_size = int(deck_size[0]['deck_size'])

        # If not last card, redirect to next card
        if card_id == deck_size:
            return redirect('home')

        # If last card, redirect to home
        card_id += 1
        direct_to = "/view/" + deck_name + "/" + str(card_id)
        return redirect(direct_to)


@app.route('/editdeck/<deck_name>')
@login_required
def editdeck(deck_name):
    # Query for cards in the specified deck to display
    cards = db.execute('SELECT card_id, title, content, status FROM cards WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
    return render_template('editdeck.html', deck_name=deck_name, cards=cards)


@app.route('/deletecard/<card_id>', methods=['POST'])
def delete_card(card_id):

    deck_name = request.form.get('deck_name')
    if not deck_name:
        return apology('Cannot get deck_name')

    # Delete card from database
    db.execute('DELETE FROM cards WHERE user_id = ? AND deck_name = ? AND card_id = ?', session['user_id'], deck_name, card_id)
    flash('Successfully deleted card from ' + deck_name)

    # Update deck size
    deck_size = db.execute('SELECT deck_size FROM decks WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
    deck_size = int(deck_size[0]['deck_size']) - 1
    db.execute('UPDATE decks SET deck_size = ? WHERE user_id = ? AND deck_name = ?', deck_size, session['user_id'], deck_name)

    # Renumber remaining cards
    cards = db.execute('SELECT card_id, title, content FROM cards WHERE user_id = ? AND deck_name = ?', session['user_id'], deck_name)
    for i in range(len(cards)):
        db.execute('UPDATE cards SET card_id = ? WHERE user_id = ? AND deck_name = ? AND title = ? AND content = ?', i + 1, session['user_id'], deck_name, cards[i]['title'], cards[i]['content'])
    flash('Successfully renumbered cards')
    return redirect('/editdeck/' + deck_name)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for error
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
