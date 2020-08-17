# -*- coding: utf-8 -*-
"""PricingRequest models."""
import datetime as dt

from my_webapp.database import (
    Column,
    PkModel,
    db,
    reference_col,
    relationship,
)
from flask_login import current_user
from my_webapp.history_meta import Versioned

class PricingRequest(Versioned, PkModel):
    """A PricingRequest of the app."""

    __tablename__ = "pricing_requests"
    amount = Column(db.Integer, nullable=False)
    desired_rate = Column(db.Numeric, nullable=False)
    new_customer = Column(db.Boolean(), default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    version_created_at = Column(
        db.DateTime, 
        default=lambda context: context.get_current_parameters()['created_at'],
        onupdate=dt.datetime.utcnow
        )
    owner_id = Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator_id = Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    def __init__(self, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)
        
    @property
    def anticipated_profitability(self):
        """Anticipated profitability"""
        return round(self.amount * 0.01, 2)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<PricingRequest {self.id}>"
