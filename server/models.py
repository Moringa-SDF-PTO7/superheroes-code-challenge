from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)

    # Relationship to HeroPower
    powers = db.relationship('HeroPower', back_populates='hero', cascade="all, delete-orphan")

    @validates('name', 'super_name')
    def validate_name(self, key, value):
        if not value or len(value) == 0:
            raise ValueError(f"{key} cannot be empty.")
        return value


class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)  # Made description optional

    # Relationship to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all, delete-orphan")

    @validates('name', 'description')
    def validate_power(self, key, value):
        if not value or len(value) == 0:
            raise ValueError(f"{key} cannot be empty.")
        return value


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Integer, nullable=False, default=0)  # Default strength to 0
    
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        if value is None or value < 0:  # Ensure strength is a non-negative integer
            raise ValueError(f"{key} must be a non-negative integer.")
        return value
