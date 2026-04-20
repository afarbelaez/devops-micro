import os

# Setear variables de entorno ANTES de importar la app
# Esto evita que Config lea DATABASE_URL=None del entorno real
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['STATIC_TOKEN'] = 'test-token'
os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret'

import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Crea la app Flask con SQLite en memoria — sin depender de RDS."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'STATIC_TOKEN': 'test-token',
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente HTTP de prueba."""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Header de autorización válido."""
    return {'Authorization': 'Bearer test-token'}


@pytest.fixture
def sample_payload():
    """Body válido para POST /blacklists."""
    return {
        'email': 'spammer@test.com',
        'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
        'blocked_reason': 'Envio de spam masivo'
    }
