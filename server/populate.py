from app import app, db, Hero, Power

with app.app_context():
    # Create tables
    db.create_all()

    # Add sample powers
    power1 = Power(name="Flight", description="Ability to fly.")
    power2 = Power(name="Super Strength", description="Incredible physical strength.")
    power3 = Power(name="Invisibility", description="Ability to become invisible.")

    db.session.add_all([power1, power2, power3])
    db.session.commit()

    # Add sample heroes
    hero1 = Hero(name="Superman", super_name="Clark Kent")
    hero2 = Hero(name="Batman", super_name="Bruce Wayne")
    hero3 = Hero(name="Wonder Woman", super_name="Diana Prince")
    hero4 = Hero(name="Flash", super_name="Barry Allen")
    hero5 = Hero(name="Green Lantern", super_name="Hal Jordan")
    hero6 = Hero(name="Iron Man", super_name="Tony Stark")
    hero7 = Hero(name="Captain America", super_name="Steve Rogers")
    hero8 = Hero(name="Spider-Man", super_name="Peter Parker")
    hero9 = Hero(name="Thor", super_name="Thor Odinson")
    hero10 = Hero(name="Hulk", super_name="Bruce Banner")

    db.session.add_all([hero1, hero2, hero3, hero4, hero5, hero6, hero7, hero8, hero9, hero10])
    db.session.commit()

    print("Sample data added successfully!")