from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask import url_for

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return 'Hello World!'


@app.route("/user/<name>")
def get_user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    # Tips:返回的是tuple
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run()


print(url_for('/'))
