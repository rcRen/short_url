from flask import render_template
from src import create_app
from dotenv import load_dotenv
import os

load_dotenv()
app = create_app()


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
