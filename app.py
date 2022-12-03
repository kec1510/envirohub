import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, PasswordField, validators

from config import login_required

from programs.forecasts import weather_aq_forecast
from programs.news import get_news

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

CAMBRIDGE_LAT, CAMBRIDGE_LON = 42.3736, -71.1097

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def get_db_connection():
    conn = sqlite3.connect('envirohub.db')
    conn.row_factory = sqlite3.Row
    return conn

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match.')
    ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=25)])
    # email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Length(min=10, max=40),
        validators.DataRequired(),
    ])

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template('index.html', data=weather_aq_forecast(CAMBRIDGE_LAT, CAMBRIDGE_LON), article_lst=get_news('climate change'))

# News Search
@app.route("/news", methods=["GET", "POST"])
@login_required
def news():
    if request.method == 'POST':
        search_q = request.form.get("search_q")

        if not search_q:
            return render_template('400.html', message='Invalid search input. Please try again.')
        
        results = get_news(search_q)

        return render_template('news_results.html', query=search_q, article_lst=results)

    else:
        return render_template('news.html')

# Forecasts
@app.route("/forecasts", methods=["GET", "POST"])
@login_required
def forecasts():
    if request.method == 'POST':
        user_id = session.get("user_id")
        lat_input = request.form.get("lat")
        lon_input = request.form.get("lon")

        if not lat_input or not lon_input:
            return render_template('400.html', message='Invalid forecast input. Please try again.')
        
        results = weather_aq_forecast(lat_input, lon_input)
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO fc_history (user_id, lat, lon, temp, weather, aqi) VALUES (?, ?, ?, ?, ?, ?)", 
                       (user_id, lat_input, lon_input, results['Temperature'], results['Weather'], results['Air Quality Index']))
        except Exception as e:
            print(e)
            return render_template('400.html', message='Invalid forecast input. Please try again.')

        conn.commit()
        conn.close()

        return render_template('forecast_results.html', lat=lat_input, lon=lon_input, data=results)

    else:
        return render_template('forecasts.html', data=weather_aq_forecast(CAMBRIDGE_LAT, CAMBRIDGE_LON))

# Forecast History
@app.route("/history", methods=["GET"])
@login_required
def history():
    user_id = session.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()

    fc_history = cur.execute("SELECT datetime, lat, lon, temp, weather, aqi FROM fc_history WHERE user_id = ? ORDER BY datetime DESC", (user_id,)).fetchall()
    conn.commit()
    conn.close()
    
    return render_template('history.html', data=fc_history)

# Registration, Login, Logout
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('400.html', message='Invalid registration. Please try again.')

        user_, email_, pass_, = form.username.data, form.email.data, form.password.data
        
        if not user_ or not email_ or not pass_:
            return render_template('400.html', message='Invalid registration. Please try again.')

        # Add username and hashed password to database
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", (user_, email_, generate_password_hash(pass_)))
        except ValueError:
            return render_template('400.html', message='Invalid registration: username already exists. Please try again.')


        conn.commit()

        # Close database connection and redirect user to home page
        conn.close()

        flash('Thanks for registering')
        return redirect(url_for('login'))

    else:
        # if the request method is "GET", return empty registration form
        return render_template("register.html", reg_form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    form = LoginForm(request.form)
    if request.method == "POST":
        if not form.validate():
            return render_template('400.html', message='Invalid login. Please try again.')
        
        user_, pass_, = form.username.data, form.password.data
        if not user_ or not pass_:
            return render_template('400.html', message='Please enter your username and password.')

        # Query database for username
        conn = get_db_connection()
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (user_,)).fetchall()
        conn.commit()
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], pass_):
            return render_template('400.html', message='Invalid login. Please try again.')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        conn.close()
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", log_form=form)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == '__main__':
    app.run(port='3000', debug=True)

