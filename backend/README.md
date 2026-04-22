#Instructions on how to demo

To test for query on local machine, run 'run.py' with a manual query such as:
"http://127.0.0.1:5000/search?q=coding"


For a better demonstration:
1. run 'seed.py'
2. run 'seed_test.py'
3. Open up the library.db in SQLite browser to view databases and ERD.

seed.py will load dummy data into our databases; the User database will fill with 5 users, 50 books will be fetched from our google books API and loaded inside the Book database.

seed_test.py will return the first user and their corresponding relationship with the Books database. 

Open up the library.db (preferably in SQLite browser) to cross verify the results of the seed_test.py

