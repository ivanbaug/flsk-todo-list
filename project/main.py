from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

CONFIG_FILE = "config.py"


# Setup app
app = Flask(__name__)
app.config.from_pyfile(CONFIG_FILE)


@app.route("/")
def index():
    # posts = BlogPost.query.all()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
