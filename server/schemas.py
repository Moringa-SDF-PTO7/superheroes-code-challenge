from marshmallow import Schema, fields, validates
from models import Hero, Power, HeroPower

class HeroSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    super_name = fields.Str(required=True)
    powers = fields.List(fields.Nested('HeroPowerSchema', exclude=('hero',)))

class PowerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)

class HeroPowerSchema(Schema):
    id = fields.Int(dump_only=True)
    strength = fields.Str(required=True)
    hero_id = fields.Int(required=True)
    power_id = fields.Int(required=True)
    hero = fields.Nested(HeroSchema, only=["id", "name", "super_name"])
    power = fields.Nested(PowerSchema, only=["id", "name", "description"])