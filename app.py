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

# Display custom 404 error page stored in the 404.html template
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Helper function for accessing the database to insert or select entries
def get_db_connection():
    conn = sqlite3.connect('envirohub.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create registration form via WTForms package
# establish minimum and maximum lengths for each field
# ensure that password and confirmation match
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match.')
    ])
    confirm = PasswordField('Confirm Password')

# Create login form via WTForms package
# establish same minimum and maximum lengths for each field
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=25)])
    password = PasswordField('Password', [
        validators.Length(min=10),
        validators.DataRequired(),
    ])

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Return EnviroHub Dashboard 
    # Pass in the latitude and longitude for Cambridge, MA to generate
    # weather and air quality info for the dashboard
    # Pass in 'climate change' as the query to generate news results for the dashboard
    return render_template('index.html', data=weather_aq_forecast(CAMBRIDGE_LAT, CAMBRIDGE_LON), article_lst=get_news('climate change'))

# News Search
@app.route("/news", methods=["GET", "POST"])
@login_required
def news():
    # Process form inputs upon POST request
    if request.method == 'POST':
        # Store user's desired search query
        search_q = request.form.get("search_q")

        # Throw error if no form data
        if not search_q:
            return render_template('400.html', message='Invalid search input. Please try again.')
        
        # Source news results using get_news() method specified in programs/news.py
        results = get_news(search_q)

        # Display news results
        return render_template('news_results.html', query=search_q, article_lst=results)

    # Return news form upon GET request
    else:
        return render_template('news.html')

# Forecasts
@app.route("/forecasts", methods=["GET", "POST"])
@login_required
def forecasts():
    # Process form input upon POST request
    if request.method == 'POST':
        # Store user id and form inputs
        user_id = session.get("user_id")
        lat_input = request.form.get("lat")
        lon_input = request.form.get("lon")

        # Throw error if no data in form
        if not lat_input or not lon_input:
            return render_template('400.html', message='Invalid forecast input. Please try again.')
        
        # Use weather_aq_forecast() method (specified in programs/forecasts.py)
        # Get forecasts based on user-specified latitude and longitude
        results = weather_aq_forecast(lat_input, lon_input)

        # Add forecast query to database for history functionality
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO fc_history (user_id, lat, lon, temp, weather, aqi) VALUES (?, ?, ?, ?, ?, ?)", 
                       (user_id, lat_input, lon_input, results['Temperature'], results['Weather'], results['Air Quality Index']))
        except Exception as e:
            return render_template('400.html', message='Invalid forecast input. Please try again.')
       
        # Execute database insertion
        conn.commit()

        # Close database connection and display results
        conn.close()
        return render_template('forecast_results.html', lat=lat_input, lon=lon_input, data=results)

    # Return forecast form upon GET request
    else:
        return render_template('forecasts.html', data=weather_aq_forecast(CAMBRIDGE_LAT, CAMBRIDGE_LON))

# Forecast History
@app.route("/history", methods=["GET"])
@login_required
def history():
    # Get user's id to return appropriate database entries
    user_id = session.get("user_id")

    # connect to SQLite database
    conn = get_db_connection()
    cur = conn.cursor()

    # select relevant information from database to display
    fc_history = cur.execute("SELECT datetime, lat, lon, temp, weather, aqi FROM fc_history WHERE user_id = ? ORDER BY datetime DESC", (user_id,)).fetchall()
    conn.commit()

    # close database connection
    conn.close()
    
    # display the user's forecast history data
    return render_template('history.html', data=fc_history)

# Registration, Login, Logout
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegistrationForm(request.form)
    
    # Process form input upon POST request
    if request.method == 'POST':
        # Verify that entered credentials met all requirements via WTForms
        if not form.validate():
            return render_template('400.html', message='Invalid registration. Please try again.')

        user_, email_, pass_, = form.username.data, form.email.data, form.password.data
        
        # Return error if no data in submission
        if not user_ or not email_ or not pass_:
            return render_template('400.html', message='Invalid registration. Please try again.')

        # Add username and hashed password to database
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", (user_, email_, generate_password_hash(pass_)))
        except ValueError:
            return render_template('400.html', message='Invalid registration: username already exists. Please try again.')

        # Execute database insertion
        conn.commit()

        # Close database connection and redirect user to login page
        conn.close()

        flash('Thanks for registering')
        return redirect(url_for('login'))

    # Return registration form upon GET request
    else:
        return render_template("register.html", reg_form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    form = LoginForm(request.form)

    # Process form input upon POST request
    if request.method == "POST":
        # Verify that entered credentials met all requirements via WTForms
        if not form.validate():
            return render_template('400.html', message='Invalid login. Please try again.')
        
        user_, pass_, = form.username.data, form.password.data
        
        # Return error if no data in submission
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

        # Close database connection and redirect user to home page
        conn.close()
        return redirect("/")

    # Return login form upon GET request
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

