from datetime import datetime
from flask import render_template, session, \
    url_for, redirect, current_app

from . import main
from .forms import NameForm
from ..models import User
from .. import db
from ..email import send_mail


@main.route('/', methods=["GET", "POST"])
def index():
    var_form = NameForm()
    if var_form.validate_on_submit():
        query_result = User.query.filter_by(username=var_form.name.data).first()
        if query_result is None:
            new_user = User(username=var_form.name.data)
            db.session.add(new_user)
            db.session.commit()
            session["known"] = False
            if current_app.config["FLASKY_ADMIN"]:
                foo = send_mail(current_app.config["FLASKY_ADMIN"], "New User", "mail/new_user", user=new_user)
                print(foo)
        else:
            session["known"] = True
        session["name"] = var_form.name.data
        var_form.name.data = ""
        return redirect(url_for(".index"))
    return render_template("index.html", current=datetime.utcnow(),
                           name=session.get("name"),
                           known=session.get("known", False), form=var_form)


@main.route("/user/<name>")
def get_user(name):
    return render_template("user.html", name=name)
