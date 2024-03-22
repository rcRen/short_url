from flask import render_template
from src import create_app
import os
from dotenv import load_dotenv

load_dotenv()
# basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.getenv("CONFIG_MODE"))


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run()
