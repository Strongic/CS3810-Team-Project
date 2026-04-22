from app import create_app
from dotenv import load_dotenv
import os

#load api key
load_dotenv()

#create flask app instance
app = create_app()

#start server
if __name__ == "__main__":
    app.run(debug=True, port=5000) #debug=True allows the server to auto-reload when you change code