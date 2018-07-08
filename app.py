from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import session, url_for, redirect, flash


class NameForm(Form):
    name = StringField("what is your name?", validators=[Required()])
    submit = SubmitField("Submit")


app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string."
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=["GET", "POST"])
def index():
    var_form = NameForm()
    if var_form.validate_on_submit():
        old_name = session.get("var_name")
        if old_name is not None and old_name != var_form.name.data:
            flash("it is different name!")
        session["var_name"] = var_form.name.data
        return redirect(url_for("index"))
    return render_template("index.html", current=datetime.utcnow(), name=session.get("var_name"), form=var_form)


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

print(app.url_map)
