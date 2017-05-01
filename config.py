'''
Define the configuration parameters for the database connection.

For initial development, MAMP was used, but these connection settings can be
altered to another server. Update the parameters as necessary. For issues,
see the database server's documentation.
'''
import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    # Uncomment next line if using a network connection instead of socket
    # 'host': 'localhost:8889',
    # Comment out next line if using a network connection instead of socket
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'raise_on_warnings': True,
}

db = mysql.connector.connect(**config)
