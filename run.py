from flask import render_template
from src import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app(os.getenv("CONFIG_MODE"))


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/code")
def code():
    return render_template('short_code.html')


if __name__ == "__main__":
    app.run()
