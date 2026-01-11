from flask import Flask, request
from flask_restful import Api, Resource
from db import db
from flask_migrate import Migrate
import os
from models import Hero, Power, HeroPower

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(BASE_DIR, 'superheroes.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


# Resources / Routes
class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [hero.to_dict(only=('id','name','super_name')) for hero in heroes], 200

class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if not hero:
            return {"error": "Hero not found"}, 404
        return hero.to_dict(), 200

class Powers(Resource):
    def get(self):
        return [power.to_dict() for power in Power.query.all()], 200

class PowerByID(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if not power:
            return {"error": "Power not found"}, 404
        return power.to_dict(), 200

    def patch(self, id):
        power = Power.query.get(id)
        if not power:
            return {"error": "Power not found"}, 404
        try:
            power.description = request.json['description']
            db.session.commit()
            return power.to_dict(), 200
        except ValueError:
            return {"errors": ["validation errors"]}, 400

class HeroPowers(Resource):
    def post(self):
        try:
            hp = HeroPower(
                strength=request.json['strength'],
                hero_id=request.json['hero_id'],
                power_id=request.json['power_id']
            )
            db.session.add(hp)
            db.session.commit()
            return hp.to_dict(), 201
        except ValueError:
            return {"errors": ["validation errors"]}, 400


api.add_resource(Heroes, '/heroes')
api.add_resource(HeroByID, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowerByID, '/powers/<int:id>')
api.add_resource(HeroPowers, '/hero_powers')


if __name__ == "__main__":
    app.run(port=5555, debug=True)





