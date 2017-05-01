'''
Create the soundcollide app's database and table.

Example usage:
    $ python make_db.py

Attributes:
    DB_NAME (string): The name of the database
    TABLES (dict): The tables to be created within the database
    cursor (MySQLCursor): Cursor for the database
'''
import mysql.connector
from mysql.connector import errorcode
from soundcollide.config import db

DB_NAME = 'users'

TABLES = {}

TABLES['users'] = (
    '''CREATE TABLE `users` (
        `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
        `username` varchar(20) NOT NULL DEFAULT '',
        `email` varchar(64) NOT NULL DEFAULT '',
        PRIMARY KEY(`id`),
        UNIQUE KEY `unique_username` (`username`),
        UNIQUE KEY `unique_email` (`email`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8'''
)

cursor = db.cursor()


def create_database(cursor):
    '''Create database'''
    try:
        cursor.execute(
            f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'"
        )
    except mysql.connector.Error as err:
        print(f'Failed creating database with error: {err}')
        exit(1)


def main():
    '''Create database and tables'''
    try:
        db.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            db.database = DB_NAME
        else:
            print(err)
            exit(1)

    for name, ddl in TABLES.items():
        try:
            print(f'Creating table {name}: ', end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('already exists.')
        else:
            print('OK.')
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
