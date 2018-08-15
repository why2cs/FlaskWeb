from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import session, url_for, redirect, flash

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os


class NameForm(FlaskForm):
    name = StringField("what is your name?", validators=[Required()])
    submit = SubmitField("Submit")


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string."
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

db.create_all()


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role> {}".format(self.name)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User {}".format(self.username)


@app.route('/', methods=["GET", "POST"])
def index():
    var_form = NameForm()
    if var_form.validate_on_submit():
        query_result = User.query.filter_by(username=var_form.name.data).first()
        if query_result is None:
            new_user = User(username=var_form.name.data)
            db.session.add(new_user)
            session["known"] = False
        else:
            session["known"] = True
        session["name"] = var_form.name.data
        var_form.name.data = ""
        return redirect(url_for("index"))
    return render_template("index.html", current=datetime.utcnow(),
                           name=session.get("name"),
                           known=session.get("known", False), form=var_form)


@app.route("/user/<name>")
def get_user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found():
    # Tips:返回的是tuple
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error():
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run()

print(app.url_map)
