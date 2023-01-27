"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicles, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#get user
@app.route('/user', methods=['GET'])
def handle_hello():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))
    return jsonify(results), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.serialize()), 200

#get characters
@app.route('/people', methods=['GET'])
def get_people():
    allPeople = Characters.query.all()
    results = list(map(lambda item: item.minSerialize(),allPeople))
    return jsonify(results), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def get_info_person(person_id):
    person = Characters.query.filter_by(id=person_id).first()
    return jsonify(person.serialize()), 200

#get planets
@app.route('/planets', methods=['GET'])
def get_planets():
    allPlanets= Planets.query.all()
    results = list(map(lambda item: item.minSerialize(),allPlanets))
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_info_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    print(planet)
    return jsonify(planet.serialize()), 200

#get vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    allVehicles = Vehicles.query.all()
    results = list(map(lambda item: item.minSerialize(),allVehicles))
    return jsonify(results), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_info_vehicle(vehicle_id):
    vehicle = Vehicles.query.filter_by(id=vehicle_id).first()
    print(vehicle)
    return jsonify(vehicle.serialize()), 200

#get user favorites
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorites.query.filter_by(userID=user_id).all()
    results = list(map(lambda item: item.serialize(),favorites))
    return jsonify(results), 200

#add a favorite planet
@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    #Add function from the docs
    planeta = Planets.query.filter_by(id=planet_id).first().serialize()
    planetName = planeta['name']
    planet = Favorites(userID = user_id , planetsName = planetName)
    print(planet)
    db.session.add(planet)
    db.session.commit()

    #Get user favorites
    favorites = Favorites.query.filter_by(userID=user_id).all()
    results = list(map(lambda item: item.serialize(),favorites))
    return jsonify(results), 201

#add a favorite person
@app.route('/user/<int:user_id>/favorites/people/<int:person_id>', methods=['POST'])
def add_person_favorite(user_id, person_id):
    #Add function from the docs
    persona = Characters.query.filter_by(id=person_id).first().serialize()
    personName = persona['name']
    person = Favorites(userID = user_id , charactersName = personName)
    db.session.add(person)
    db.session.commit()

    #Get user favorites
    favorites = Favorites.query.filter_by(userID=user_id).all()
    results = list(map(lambda item: item.serialize(),favorites))
    return jsonify(results), 201

#add a favorite vehicle
@app.route('/user/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['POST'])
def add_vehicle_favorite(user_id, vehicle_id):
    #Add function from the docs
    vehiculo = Vehicles.query.filter_by(id=vehicle_id).first().serialize()
    vehicleName = vehiculo['name']
    vehicle = Favorites(userID = user_id , vehiclesName = vehicleName)
    db.session.add(vehicle)
    db.session.commit()
    #Get user favorites
    favorites = Favorites.query.filter_by(userID=user_id).all()
    results = list(map(lambda item: item.serialize(),favorites))
    return jsonify(results), 201

@app.route('/user', methods=['POST'])
def add_new_user():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))
    request_body = json.loads(request.data)
    results.append(request_body)
    return jsonify(results), 201

#DELETE
#Delete user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    return jsonify("User deleted"), 201

#Delete planet favorites from user
@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    planeta = Planets.query.filter_by(id=planet_id).first().serialize()
    planetName = planeta['name']
    favorite_planet = Favorites.query.filter_by(userID=user_id, planetsName = planetName).first()
    print(favorite_planet)
    db.session.delete(favorite_planet)
    db.session.commit()
    favorites = Favorites.query.filter_by(userID=user_id).all()
    results = list(map(lambda item: item.serialize(),favorites))
    return jsonify(results), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
