# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class EditForm(FlaskForm):
    """Edit form."""

    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(EditForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(EditForm, self).validate()
        if not initial_validation:
            return False
        
        # Unique email
        user = User.query.filter_by(email=self.email.data).first()
        if user and user!=current_user:
            self.email.errors.append("Email already registered")
            return False
        
        return True
