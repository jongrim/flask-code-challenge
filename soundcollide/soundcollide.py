from flask import Flask, request, make_response
from config import config
import mysql


app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'


@app.route('/new-profile/', methods=['POST'])
def new_profile():
    '''Validate input for a new profile and return the appropriate error code
    or database response.

    A successful post must have a unique username, unique email, valid zipcode,
    password of at least 6 characters, and a matching confirmation password.

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
        'INSERT INTO user (username, email, zipcode) VALUES (%s, %s, %s)'
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

    Returns:
        Response: A 201 status code is returned if the project is successfully
            added. If not a 400 status code is returned indicating the operation
            was not successful.
    '''
    project = request.form['project']
    username = request.form['username']

    db = get_database_connection()
    cursor = db.cursor()

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

    add_project = (
        'INSERT INTO projects (project, user) VALUES (%s, %s)'
    )

    try:
        cursor.execute(add_project, (project, user_id))
    except mysql.connector.errors.IntegrityError as err:
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
        Connection: A connection to the database
    '''
    db = mysql.connector.connect(**config)
    db.database = 'users'
    return db
