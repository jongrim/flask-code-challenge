from flask import Flask, request, make_response
from config import db
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

    db.database = 'users'
    cursor = db.cursor()
    try:
        cursor.execute(add_user, (username, email, zipcode))
    except mysql.connector.errors.IntegrityError as err:
        return make_response((f'Failed to add entry with error: {err}', 500))
    else:
        db.commit()

    cursor.close()
    db.close()

    return make_response((f'User, {username}, added', 201))


@app.route('/profile/<int:id>')
def get_profile(id):
    '''Retrieve the profile for the given id and return its attributes.

    Parameters:
        id (int): The id for the profile to be displayed
    '''

    db.database = 'users'
    cursor = db.cursor(dictionary=True)

    select_user = (
        'SELECT username, email, zipcode FROM user WHERE id=%s'
    )

    cursor.execute(select_user, id)
    if cursor.rowcount < 1:
        return make_response(('User not found', 200))

    row = cursor.next()
    return make_response((row['username'], 200))
