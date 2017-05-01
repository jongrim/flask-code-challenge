# Steps for configuring development environment:
Below are the necessary steps for installing and using the supplied application. For development, I used MAMP to supply the MySQL server, though this could be easily changed and instructions for how to do so are given below and noted within the code.

## Prerequisites
These instructions assume Python 3.3 or higher is installed and has the standard library, including venv, available. Python 3.6.1 was used in development of this application. These instructions also assume a basic familiarity with the terminal.

## Optional Third-Pary Downloads
- To replicate MySQL database transactions, download and install MAMP (https://www.mamp.info/en/)

## Mandatory Installation Steps
- Initialize a python virtual environment within the top soundcollide_app directory:
    - `$ python3 -m venv .`
- Activate the python virtual environment:
    - `$ source ./bin/activate`
- Install the application via the supplied setup.py file by executing the following command:
    - `(soundcollide-app) user $ pip install --editable .`
    - This step will install the application dependencies of Flask and MySQL-Connector
- Ensure MAMP or another MySQL server has been installed and is running
- Confirm that the database connection parameters in the `config.py` file are accurate, and edit as necessary. Refer to your MySQL server documentation for the appropriate server location.
- Execute the `make_db.py` file via the terminal:
    - `(soundcollide-app) user $ python make_db.py`

# Running the application
After the mandatory installation steps have been completed, the application can be ran following these steps:

- Export the FLASK_APP environment variable:
    - `(soundcollide-app) user $ export FLASK_APP=soundcollide.py`
- Move into the soundcollide package directory. See the application structure reference chart below if necessary.
- Start the Flask development server:
    - `(soundcollide-app) user $ flask run`
- Use a browser or a tool such as Postman to send requests to the defined endpoints

# Recommendations for testing
No database export is provided, so the database and tables are created empty. I recommend first testing calls to the `/new-profile/` endpoint to generate some table data, and then moving on to testing the `/profile/<id>` and `/project/` endpoints. Comments are included in the code which outline the expected parameters for each endpoint.

Note that Flask is particular about the URLs for POST requests. URLs have been defined with trailing slashes, and Flask will generate a Method Not Allowed Error if a POST request is sent to the URL without the trailing slash.

# Application folder structure
Below is a reference chart of the relevant application folders and files. Directories added by libraries or Python virtual environment are not documented, so this is not representative of every file and directory that will exist. Directories are indicated by a trailing slash, while files have file endings.

```
soundcollide_app/
|----soundcollide/
|    |----__init__.py
|    |----soundcollide.py
|----config.py
|----make_db.py
|----setup.py
|----README.md
```
