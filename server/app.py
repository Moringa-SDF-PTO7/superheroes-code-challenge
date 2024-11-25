from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from schemas import HeroSchema, PowerSchema, HeroPowerSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes_powers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
db.init_app(app)
migrate = Migrate(app, db)

hero_schema = HeroSchema()
power_schema = PowerSchema()
hero_power_schema = HeroPowerSchema()

# Route to get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return hero_schema.dump(heroes, many=True)

# Route to get a single hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = hero_schema.dump(hero)
        hero_data['powers'] = [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description, 'strength': hp.strength} for hp in hero.powers]
        return jsonify(hero_data)
    else:
        return jsonify({"error": "Hero not found"}), 404

# Route to get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return power_schema.dump(powers, many=True)

# Route to get a single power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return power_schema.dump(power)
    else:
        return jsonify({"error": "Power not found"}), 404

# Route to update a power's description
@app.route('/powers/<int:id>', methods=['PATCH'])
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

# Route to create a new hero power association
@app.route('/hero_powers', methods=['POST'])
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

# Route to add a new hero
@app.route('/add_hero', methods=['POST'])
def add_hero():
    data = request.get_json()
    name = data.get('name')
    super_name = data.get('super_name')

    if not name or not super_name:
        return jsonify({"error": "Name and Super Name are required."}), 400

    new_hero = Hero(name=name, super_name=super_name)
    db.session.add(new_hero)
    
    try:
        db.session.commit()
        return jsonify({"message": "Hero added successfully!", "id": new_hero.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# New route to display all heroes as JSON
@app.route('/display_heroes', methods=['GET'])
def display_heroes():
    heroes = Hero.query.all()
    return hero_schema.dump(heroes, many=True)  # Return heroes in JSON format

# Route to display all available routes
@app.route('/routes', methods=['GET'])
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return jsonify(routes)

if __name__ == '__main__':
    app.run(debug=True)