from flask import Blueprint, jsonify, request
from models import db, Hero, Power, HeroPower
from schemas import HeroSchema, PowerSchema, HeroPowerSchema

# Create a Blueprint for the routes
api_bp = Blueprint('api', __name__)

hero_schema = HeroSchema()
power_schema = PowerSchema()
hero_power_schema = HeroPowerSchema()

# Route to get all heroes
@api_bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return hero_schema.dump(heroes, many=True)

# Route to get a specific hero by ID
@api_bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        hero_powers = []
        for hp in hero.powers:
            hero_powers.append({
                'hero_id': hp.hero_id,
                'id': hp.id,
                'power_id': hp.power_id,
                'strength': hp.strength,
                'power': {
                    'id': hp.power.id,
                    'name': hp.power.name,
                    'description': hp.power.description
                }
            })
        hero_data = hero_schema.dump(hero)
        hero_data['hero_powers'] = hero_powers
        return jsonify(hero_data)
    else:
        return jsonify({"error": "Hero not found"}), 404

# Route to get all powers
@api_bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return power_schema.dump(powers, many=True)

# Route to get a specific power by ID
@api_bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return power_schema.dump(power)
    else:
        return jsonify({"error": "Power not found"}), 404

# Route to update a specific power by ID
@api_bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get('description')

    if not description:
        return jsonify({"errors": ["Description is required."]}), 400

    try:
        power.description = description
        db.session.commit()
        return power_schema.dump(power)
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

# Route to create a new HeroPower relationship
@api_bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not strength or not power_id or not hero_id:
        return jsonify({"errors": ["All fields are required."]}), 400

    try:
        new_hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(new_hero_power)
        db.session.commit()
        
        return hero_power_schema.dump(new_hero_power), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

# Register the blueprint in your app
def register_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')