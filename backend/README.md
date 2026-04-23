# Instructions on how to demo

## ENSURE you are running a venv and installed the requirements BEFORE attempting to run the demo. https://docs.python.org/3/library/venv.html


Make sure you are at the root of the project directory and then run:
* python -m venv
* source venv/bin/activate
* pip install -r requirements


To test the querying on your local machine, run 'run.py' with a manual query such as:
"http://127.0.0.1:5000/search?q=coding"


For an ERD demonstration:
* run 'seed.py'
* run 'seed_test.py'
* Open up the library.db in SQLite browser to view databases and ERD.

seed.py will load dummy data into our databases; the User database will fill with 5 users, 50 books will be fetched from our google books API and loaded inside the Book database.

seed_test.py will return a user and their corresponding relationship with the Books database. 

Open up the library.db (preferably in SQLite browser) to cross verify the results of the seed_test.py

