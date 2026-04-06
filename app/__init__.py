from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_restful import Api

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    from app.views import BlacklistList, BlacklistDetail
    api.add_resource(BlacklistList, '/blacklists')
    api.add_resource(BlacklistDetail, '/blacklists/<string:email>')

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    @app.route('/version')
    def version():
        return {'version': '5.0.0-immutable'}, 200

    with app.app_context():
        db.create_all()

    return app
