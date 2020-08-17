# -*- coding: utf-8 -*-
"""Pricing Desk forms."""
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import PricingRequest


class CreateForm(FlaskForm):
    """Register form."""

    amount = IntegerField(
        "Amount ($)", validators=[]
    )
    desired_rate = DecimalField(
        "Desired rate (%)", validators=[]
    )
    new_customer = BooleanField(
        "New customer ?", validators=[]
    )
    
    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(CreateForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(CreateForm, self).validate()
        if not initial_validation:
            return False
        
        # Amount positive
        if self.amount.data<=0:
            self.amount.errors.append("Amount must be greater than zero.")
            return False

        return True


