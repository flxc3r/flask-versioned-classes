# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from my_webapp.user.forms import EditForm
from my_webapp.utils import flash_errors

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    """Edit members."""
    form = EditForm(request.form)
    if form.validate_on_submit():
        current_user.update(
            email=form.email.data,
        )
        flash("Changes saved", "success")
        return redirect(url_for("user.members"))
    else:
        flash_errors(form)
    return render_template("users/edit.html", form=form)
