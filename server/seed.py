from app import app, db
from models import Hero, Power, HeroPower

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(HeroPower).delete()
        db.session.query(Hero).delete()
        db.session.query(Power).delete()

        # Create initial data
        heroes = [
            Hero(name='Kamala Khan', super_name='Ms. Marvel'),
            Hero(name='Doreen Green', super_name='Squirrel Girl'),
            Hero(name='Gwen Stacy', super_name='Spider-Gwen'),
            Hero(name='Janet Van Dyne', super_name='The Wasp'),
            Hero(name='Wanda Maximoff', super_name='Scarlet Witch'),
            Hero(name='Carol Danvers', super_name='Captain Marvel'),
            Hero(name='Jean Grey', super_name='Dark Phoenix'),
            Hero(name='Ororo Munroe', super_name='Storm'),
            Hero(name='Kitty Pryde', super_name='Shadowcat'),
            Hero(name='Elektra Natchios', super_name='Elektra')
        ]

        powers = [
            Power(name='Super Strength', description='gives the wielder super-human strengths'),
            Power(name='Flight', description='gives the wielder the ability to fly through the skies at supersonic speed'),
            Power(name='Super Human Senses', description='allows the wielder to use her senses at a super-human level'),
            Power(name='Elasticity', description='can stretch the human body to extreme lengths')
        ]

        # Add heroes and powers to the session
        db.session.add_all(heroes)
        db.session.add_all(powers)
        db.session.commit()

        # Create HeroPower relationships
        db.session.add(HeroPower(hero_id=1, power_id=1, strength='Strong'))  # Kamala Khan
        db.session.add(HeroPower(hero_id=2, power_id=2, strength='Average'))  # Doreen Green
        db.session.add(HeroPower(hero_id=3, power_id=3, strength='Weak'))  # Gwen Stacy
        db.session.commit()

        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()