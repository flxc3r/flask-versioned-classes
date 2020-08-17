# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from my_webapp.pricing_request.models import PricingRequest
PricingRequestHistory = PricingRequest.__history_mapper__.class_
from my_webapp.pricing_request.forms import CreateForm
from my_webapp.utils import flash_errors

blueprint = Blueprint("pricing_request", __name__, url_prefix="/pricing-requests", static_folder="../static")


@blueprint.route("/<int:id>", methods=["GET", "POST"])
@login_required
def read(id):
    """Read a pricing request."""
    pricing_request = PricingRequest.query.get(id)
    pricing_request_versions = PricingRequestHistory.query.filter(PricingRequestHistory.id==pricing_request.id).order_by(PricingRequestHistory.version.desc())
    return render_template("pricing_request/read.html", pricing_request=pricing_request, pricing_request_versions=pricing_request_versions)


@blueprint.route("/all")
@login_required
def read_all():
    """List pricing requests."""
    pricing_requests = PricingRequest.query.order_by(PricingRequest.version_created_at.desc()).all()
    return render_template("pricing_request/read_all.html", pricing_requests=pricing_requests)


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create pricing request."""
    form = CreateForm(request.form)
    if form.validate_on_submit():
        PricingRequest.create(
            
            amount = form.amount.data,
            desired_rate = form.desired_rate.data,
            new_customer = form.new_customer.data,
            owner_id = current_user.id,
            creator_id = current_user.id
            
        )
        flash("Pricing request created", "success")
        return redirect(url_for("pricing_request.read_all"))
    else:
        flash_errors(form)

    return render_template("pricing_request/create.html", form=form)


@blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    """Edit pricing request."""
    form = CreateForm(request.form)
    pricing_request = PricingRequest.query.get(id)
    if form.validate_on_submit():
        pricing_request.update(
            amount = form.amount.data,
            desired_rate = form.desired_rate.data,
            new_customer = form.new_customer.data,
            owner_id = current_user.id,
        )
        flash("Pricing request was updated", "success")
        return redirect(url_for("pricing_request.read", id=pricing_request.id))
    else:
        flash_errors(form)

    return render_template("pricing_request/edit.html", form=form, pricing_request=pricing_request)


# @blueprint.route("/edit", methods=['GET', 'POST'])
# @login_required
# def edit():
#     """Edit members."""
#     form = EditForm(request.form)
#     if form.validate_on_submit():
#         current_user.update(
#             email=form.email.data,
#         )
#         flash("Changes saved", "success")
#         return redirect(url_for("user.members"))
#     else:
#         flash_errors(form)
#     return render_template("users/edit.html", form=form)
