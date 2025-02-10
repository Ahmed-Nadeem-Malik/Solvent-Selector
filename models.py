from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    solvents = db.relationship('Solvent', backref='reaction', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Solvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    yield_range = db.Column(db.String(20), nullable=False)
    smiles = db.Column(db.String(200), nullable=False)
    reaction_id = db.Column(db.Integer, db.ForeignKey('reaction.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 