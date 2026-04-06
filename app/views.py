from functools import wraps
from flask import request, current_app
from flask_restful import Resource
from marshmallow import ValidationError

from app import db
from app.models import BlacklistEntry
from app.schemas import BlacklistEntryInputSchema


def token_required(f):
    """Valida que el header Authorization: Bearer <token> coincida con STATIC_TOKEN."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return {'message': 'Token de autorización requerido'}, 401
        token = auth_header[len('Bearer '):]
        if token != current_app.config['STATIC_TOKEN']:
            return {'message': 'Token inválido'}, 401
        return f(*args, **kwargs)
    return decorated


class BlacklistList(Resource):

    @token_required
    def post(self):
        schema = BlacklistEntryInputSchema()
        try:
            data = schema.load(request.get_json(force=True) or {})
        except ValidationError as err:
            return {'message': 'Datos inválidos', 'errors': err.messages}, 400

        existing = BlacklistEntry.query.filter_by(email=data['email']).first()
        if existing:
            return {'message': f"El email {data['email']} ya se encuentra en la lista negra"}, 409

        entry = BlacklistEntry(
            email=data['email'],
            app_uuid=data['app_uuid'],
            blocked_reason=data.get('blocked_reason'),
            requester_ip=request.remote_addr,
        )
        db.session.add(entry)
        db.session.commit()

        return {'message': f"El email {data['email']} fue agregado a la lista negra exitosamente"}, 201


class BlacklistDetail(Resource):

    @token_required
    def get(self, email):
        entry = BlacklistEntry.query.filter_by(email=email).first()
        if entry:
            return {'isBlacklisted': True, 'blockedReason': entry.blocked_reason}, 200
        return {'isBlacklisted': False, 'blockedReason': None}, 200
