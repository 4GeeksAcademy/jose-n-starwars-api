"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint, Response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorites, Vehicules
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods = ['GET'])
def get_people():

    try:

        people = People.query.all()

        if not people:
            return jsonify({'msg': "No se encontraron los personajes"}), 404
        

        people = list(map(lambda person: person.serialize(), people))
        return jsonify(people),201

    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500


@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    try:

        person = People.query.filter_by(id = id).first()

        if not person:
            return jsonify({'msg': f"No se encontraron el personaje {id}"}), 404
        
        return jsonify(person.serialize()),201

    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500

@app.route('/planets', methods = ['GET'])
def get_planets():

    try:

        planets = Planet.query.all()

        if not planets:
            return jsonify({'msg': "No se encontraron los planetas"}), 404
        

        planets = list(map(lambda planet: planet.serialize(), planets))
        return jsonify(planets), 201

    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    try:

        planet = Planet.query.filter_by(id = id).first()

        if not planet:
            return jsonify({'msg': "No se encontro el planeta"}), 404
        
        return jsonify(planet.serialize()), 201

    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500


@app.route('/users', methods = ['GET'])
def get_users():
    try:

        users = User.query.all()

        if not users:
            return jsonify({'msg': "No existen usuarios registrados"})

        users = list(map(lambda user: user.serialize(), users))

        return jsonify(users), 201
    
    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    try:

        favorites = Favorites.query.filter_by(user_id = user_id).all()

        if not favorites:
            return jsonify({'msg': f"El usuario {user_id} no tiene favoritos registrados"})
        
        favorites = list(map(lambda favorite: favorite.serialize(), favorites))

        return jsonify(favorites), 201

    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500
    

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_favorite_planet(user_id,planet_id):
    try:

        planet = Planet.query.filter_by(id = planet_id).first()
        user = User.query.filter_by(id = user_id).first()

        if not planet:
            return jsonify({'msg': "El planeta elegido no existe"}), 404
        if not user:
            return jsonify({'msg': "El usuario elegido no existe"}), 404

        new_favorite_planet = Favorites(user_id = user_id, planet_id = planet_id)
        db.session.add(new_favorite_planet)
        db.session.commit()

        return jsonify(new_favorite_planet.serialize()), 201
       
    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500
    
@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods = ['POST'])
def add_favorite_people(user_id, people_id):
    try:

        person = People.query.filter_by(id = people_id).first()
        user = User.query.filter_by(id = user_id).first()

        if not person:
            return jsonify({'msg': "El personaje elegido no existe"}), 404
        if not user:
            return jsonify({'msg': "El usuario elegido no existe"}), 404

        new_favorite_people = Favorites(user_id = user_id, people_id = people_id)
        db.session.add(new_favorite_people)
        db.session.commit()

        return jsonify(new_favorite_people.serialize()), 201
       
    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_favorite_people(user_id,people_id):
    try:

        favorite = Favorites.query.filter_by(people_id = people_id, user_id = user_id).first()

        if not favorite:
            return jsonify({'msg': f"No existe el personaje {people_id} en favorito del usuario {user_id}"}), 404
        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'msg': f"Personaje {people_id} eliminado satisfactoriamente de favoritos del usuario {user_id}"}) 

    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500
    
@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_favorite_planet(user_id,planet_id):

    try:

        favorite = Favorites.query.filter_by(planet_id = planet_id, user_id = user_id).first()

        if not favorite:
            return jsonify({'msg': f"No existe el planeta {planet_id} en favorito del usuario {user_id}"}), 404
        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'msg': f"Planeta {planet_id} eliminado satisfactoriamente de favoritos del usuario {user_id}"}) 

    except Exception as error:
        return jsonify({'msg': f"Ocurrio el siguiente error: {error}"}), 500
    



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
