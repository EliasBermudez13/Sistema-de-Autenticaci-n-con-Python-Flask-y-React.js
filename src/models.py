from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userName = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.userName

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "userName": self.userName,
            "firstName": self.firstName,
            "lastName": self.lastName
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    charactersName = db.Column(db.String(50), db.ForeignKey('characters.name'), nullable=True)
    vehiclesName = db.Column(db.String(50), db.ForeignKey('vehicles.name'), nullable=True)
    planetsName = db.Column(db.String(50), db.ForeignKey('planets.name'), nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "userID": self.userID,
            "characters": self.charactersName,
            "planets": self.planetsName,
            "vehicles": self.vehiclesName
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250), unique=True)
    gender = db.Column(db.String(250))
    films = db.Column(db.String(250))
    height = db.Column(db.String(250))
    mass = db.Column(db.String(250))
    hairColor = db.Column(db.String(250))
    skinColor = db.Column(db.String(250))
    eyeColor = db.Column(db.String(250))
    birthYear = db.Column(db.String(250))
    starships = db.Column(db.String(250))
    created = db.Column(db.String(250))
    edited = db.Column(db.String(250))
    species = db.Column(db.String(250))
    vehicles = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='characters', lazy=True)
    def __repr__(self):
        return '<Characters %r>' % self.id

    def minSerialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hairColor": self.hairColor,
            "gender": self.gender
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "films": self.films,
            "height": self.height,
            "mass": self.mass,
            "hairColor": self.hairColor,
            "skinColor": self.skinColor,
            "eyeColor": self.eyeColor,
            "birthYear": self.birthYear,
            "starships": self.starships,
            "created": self.created,
            "edited": self.edited,
            "species": self.species,
            "vehicles": self.vehicles,
            "homeworld": self.homeworld
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    climate = db.Column(db.String(250))
    created = db.Column(db.String(250))
    diameter = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    films = db.Column(db.String(250))
    orbitalPeriod = db.Column(db.String(250))
    population = db.Column(db.String(250))
    residents = db.Column(db.String(250))
    rotationPeriod = db.Column(db.String(250))
    surfaceWater = db.Column(db.String(250))
    edited = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='planets', lazy=True)
    def __repr__(self):
        return '<Planets %r>' % self.id

    def minSerialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "created": self.created,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbitalPeriod": self.orbitalPeriod,
            "population": self.population,
            "residents": self.residents,
            "rotationPeriod": self.rotationPeriod,
            "surfaceWater": self.surfaceWater,
            "terrain": self.terrain,
            "films": self.films,
            "edited": self.edited
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250), unique=True)
    cargoCapacity = db.Column(db.String(250))
    consumables = db.Column(db.String(250))
    costInCredits = db.Column(db.String(250))
    created = db.Column(db.String(250))
    crew = db.Column(db.String(250))
    length = db.Column(db.String(250))
    manufactured = db.Column(db.String(250))
    maxAtmSpeed = db.Column(db.String(250))
    model = db.Column(db.String(250))
    passengers = db.Column(db.String(250))
    edited = db.Column(db.String(250))
    films = db.Column(db.String(250))
    vehicleClass = db.Column(db.String(250))
    pilots = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='vehicles', lazy=True)
    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def minSerialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargoCapacity": self.cargoCapacity,
            "consumables": self.consumables,
            "costInCredits": self.costInCredits,
            "created": self.created,
            "crew": self.crew,
            "length": self.length,
            "manufactured": self.manufactured,
            "maxAtmSpeed": self.maxAtmSpeed,
            "model": self.model,
            "passengers": self.passengers,
            "films": self.films,
            "vehicleClass": self.vehicleClass,
            "pilots": self.pilots,
            "edited": self.edited
        }        
