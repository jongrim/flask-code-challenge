'''
Instantiate the Flask app and provide views for the application.

This is the main module of the soundcollide package and is the point where
the Flask object is instantiated. This module also defines the views available
and performs the various database calls necessary for inserting or selecting
data.

Attributes:
    app (Flask): The Flask object.

Functions:
    index (route): Matches requests for the root of the application.
    new_profile (route): Creates a new profile based on supplied data from
        a form. Supports only POST requests.
    get_profile (route): Gets a profile matching a supplied id and returns
        the profile's attributes.
    add_project (route): Takes data from a form and saves a new project
        associated with an already existing user.
    get_database_connection: Returns a connection to the database.
'''
from flask import Flask, request, make_response
from config import config
import mysql


app = Flask(__name__)  # Uses the name of the module for instatiating the object


@app.route('/')
def index():
    return 'OK'


@app.route('/new-profile/', methods=['POST'])
def new_profile():
    '''Validate input for a new profile and return the appropriate error code
    or database response.

    A successful post must have a unique username, unique email, valid zipcode,
    password of at least 6 characters, and a matching confirmation password.

    Form Parameters:
        password (string): The user's supplied password. Must be at least 6
            characters.
        confirm_password (string): Reentry of the password. Must match the
            password value.
        username (string): The user's desired username. The database forces
            unique entries only.
        email (string): The user's email. The database forces unique entries
            only.
        zipcode (string): The user's zipcode. Must be 5 characters and a string
            of all digits.

    Returns:
        Response: Message and status code are set using make_response()
            depedning on the circumstances of the response.
    '''
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    username = request.form['username']
    email = request.form['email']
    zipcode = request.form['zipcode']

    if password != confirm_password or len(password) < 6:
        return make_response(("Invalid password or passwords don't match", 400))
    elif len(zipcode) != 5 or not zipcode.isdigit():
        return make_response(('Invalid zipcode', 400))

    add_user = (
        'INSERT INTO users (username, email, zipcode) VALUES (%s, %s, %s)'
    )

    db = get_database_connection()
    cursor = db.cursor()
    try:
        cursor.execute(add_user, (username, email, zipcode))
    except mysql.connector.errors.IntegrityError as err:
        # The database enforces unique entries for username and email
        # Duplicate entries will raise an IntegrityError
        return make_response((f'Failed to add entry with error: {err}', 500))
    else:
        db.commit()
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

    return make_response((f'User, {username}, added', 201))


@app.route('/profile/<int:id>/')
def get_profile(id):
    '''Retrieve the profile for the given id and return its attributes.

    Parameters:
        id (int): The id for the profile to be displayed.

    Returns:
        Response: If the id is valid, the username, email, and zipcode are
            rendered as a response. If not, a message is rendered that no
            result was not found.
    '''
    db = get_database_connection()
    cursor = db.cursor(dictionary=True)

    select_user = (
        'SELECT username, email, zipcode FROM users WHERE id = %s'
    )

    cursor.execute(select_user, (id,))

    try:
        row = cursor.next()
    except StopIteration:
        return make_response(('No result found', 404))
    else:
        username = row['username']
        email = row['email']
        zipcode = row['zipcode']
        return make_response((f'''
            <p>Username: {username}</p>
            <p>Email: {email}</p>
            <p>Zipcode: {zipcode}</p>
        ''', 200))
    finally:
        cursor.close()
        db.close()
    return make_response((row['username'], 200))


@app.route('/project/', methods=['POST'])
def add_project():
    '''Saves a new project to a user id, if available.

    Form Parameters:
        project (string): A text string describing the project.
        username (string): The username to which the project should be saved.

    Returns:
        Response: A 201 status code is returned if the project is successfully
            added. If not a 400 status code is returned indicating the
            operation was not successful.
    '''
    project = request.form['project']
    username = request.form['username']

    db = get_database_connection()
    cursor = db.cursor()

    # Verify the user is valid and exists
    select_user = (
        'SELECT id FROM users WHERE username = %s'
    )

    cursor.execute(select_user, (username,))

    try:
        row = cursor.next()
    except StopIteration:
        return make_response(('No matching user found', 404))
    else:
        user_id = row[0]

    # Add the project to the projects table with a reference to the user
    add_project = (
        'INSERT INTO projects (project, user) VALUES (%s, %s)'
    )

    try:
        cursor.execute(add_project, (project, user_id))
    except mysql.connector.errors.IntegrityError as err:
        # Foreign key constraint will raise IntegrityError
        return make_response((f'Failed to add entry with error: {err}', 500))
    else:
        db.commit()
    finally:
        cursor.close()
        db.close()

    return make_response((f'Project saved to user, {username}', 201))


def get_database_connection():
    '''Build a database connection using the imported configuration.

    Returns:
        Connection: A connection to the database.
    '''
    db = mysql.connector.connect(**config)
    db.database = 'users'
    return db
