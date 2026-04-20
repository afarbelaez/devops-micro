"""
Pruebas unitarias del microservicio Blacklist.
Usa SQLite en memoria — no requiere conexion a RDS.
"""
import json
import pytest


# ---------------------------------------------------------------------------
# POST /blacklists
# ---------------------------------------------------------------------------

class TestPostBlacklist:

    def test_agregar_email_exitoso(self, client, auth_headers, sample_payload):
        """30% - Endpoint POST: debe retornar 201 al agregar un email valido."""
        response = client.post(
            '/blacklists',
            data=json.dumps(sample_payload),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 999  # FORZAR FALLO: codigo de respuesta incorrecto
        data = response.get_json()
        assert 'message' in data
        assert sample_payload['email'] in data['message']

    def test_agregar_email_duplicado(self, client, auth_headers, sample_payload):
        """30% - Endpoint POST: debe retornar 409 si el email ya existe."""
        # Primer insert
        client.post(
            '/blacklists',
            data=json.dumps(sample_payload),
            content_type='application/json',
            headers=auth_headers
        )
        # Segundo insert con el mismo email
        response = client.post(
            '/blacklists',
            data=json.dumps(sample_payload),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 409
        data = response.get_json()
        assert 'message' in data

    def test_agregar_sin_token(self, client, sample_payload):
        """30% - Endpoint POST: debe retornar 401 si no se envia token."""
        response = client.post(
            '/blacklists',
            data=json.dumps(sample_payload),
            content_type='application/json'
        )
        assert response.status_code == 401

    def test_agregar_token_invalido(self, client, sample_payload):
        """30% - Endpoint POST: debe retornar 401 si el token es incorrecto."""
        response = client.post(
            '/blacklists',
            data=json.dumps(sample_payload),
            content_type='application/json',
            headers={'Authorization': 'Bearer token-incorrecto'}
        )
        assert response.status_code == 401

    def test_agregar_email_formato_invalido(self, client, auth_headers):
        """30% - Endpoint POST: debe retornar 400 si el email no es valido."""
        payload = {
            'email': 'esto-no-es-un-email',
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(payload),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_agregar_sin_campos_requeridos(self, client, auth_headers):
        """30% - Endpoint POST: debe retornar 400 si faltan campos obligatorios."""
        response = client.post(
            '/blacklists',
            data=json.dumps({'email': 'solo@email.com'}),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_agregar_sin_blocked_reason(self, client, auth_headers):
        """30% - Endpoint POST: blocked_reason es opcional, debe retornar 201."""
        payload = {
            'email': 'sinrazon@test.com',
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(payload),
            content_type='application/json',
            headers=auth_headers
        )
        assert response.status_code == 201


# ---------------------------------------------------------------------------
# GET /blacklists/{email}
# ---------------------------------------------------------------------------

class TestGetBlacklist:

    def test_email_en_lista_negra(self, client, auth_headers, sample_payload):
        """30% - Endpoint GET: debe retornar isBlacklisted=True si el email existe."""
        # Insertar primero
        client.post(
            '/blacklists',
            data=json.dumps(sample_payload),
            content_type='application/json',
            headers=auth_headers
        )
        # Consultar
        response = client.get(
            f"/blacklists/{sample_payload['email']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['isBlacklisted'] is True
        assert data['blockedReason'] == sample_payload['blocked_reason']

    def test_email_no_en_lista_negra(self, client, auth_headers):
        """30% - Endpoint GET: debe retornar isBlacklisted=False si el email no existe."""
        response = client.get(
            '/blacklists/limpio@test.com',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['isBlacklisted'] is False
        assert data['blockedReason'] is None

    def test_get_sin_token(self, client):
        """30% - Endpoint GET: debe retornar 401 si no se envia token."""
        response = client.get('/blacklists/cualquier@email.com')
        assert response.status_code == 401

    def test_get_token_invalido(self, client):
        """30% - Endpoint GET: debe retornar 401 si el token es incorrecto."""
        response = client.get(
            '/blacklists/cualquier@email.com',
            headers={'Authorization': 'Bearer token-malo'}
        )
        assert response.status_code == 401

    def test_get_blocked_reason_none_cuando_no_se_proporciona(self, client, auth_headers):
        """30% - Endpoint GET: blockedReason debe ser None si no se definio razon."""
        payload = {
            'email': 'sinrazon2@test.com',
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000'
        }
        client.post(
            '/blacklists',
            data=json.dumps(payload),
            content_type='application/json',
            headers=auth_headers
        )
        response = client.get('/blacklists/sinrazon2@test.com', headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['blockedReason'] is None


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

class TestHealth:

    def test_health_retorna_ok(self, client):
        """Endpoint /health: debe retornar 200 con status ok."""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.get_json()['status'] == 'ok'


# ---------------------------------------------------------------------------
# GET /version
# ---------------------------------------------------------------------------

class TestVersion:

    def test_version_retorna_string(self, client):
        """Endpoint /version: debe retornar 200 con campo version."""
        response = client.get('/version')
        assert response.status_code == 200
        data = response.get_json()
        assert 'version' in data
        assert isinstance(data['version'], str)
