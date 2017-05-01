'''Define configuration parameters for the database connection.'''
import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'raise_on_warnings': True,
}

db = mysql.connector.connect(**config)
