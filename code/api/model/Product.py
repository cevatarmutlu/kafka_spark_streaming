from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from datetime import datetime

db = SQLAlchemy()

@dataclass
class ProductView(db.Model):
    id: int
    userid: int
    productid: int
    source: str
    timestamp: datetime

    __tablename__ = 'product_view'

    id          = db.Column(db.Integer, primary_key=True)
    userid        = db.Column(db.Integer, nullable=False)
    productid   = db.Column(db.Integer, nullable=False)
    source        = db.Column(db.String(50), nullable=True)
    timestamp         = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'product_view(' \
            f'id={self.id}, ' \
            f'userid={self.userid}, productid={self.productid}, source={self.source} timestamp={self.timestamp}'