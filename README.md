# Microservicio de Lista Negra de Emails

**Entrega 1 – DEVOPS | Universidad de los Andes**
**Equipo:** Andrés Felipe Arbeláez Ríos · Josse Restrepo

---

## Descripción

Microservicio REST para la gestión de la lista negra global de emails de una organización. Permite agregar emails a la lista negra y consultar si un email está bloqueado.

Desplegado en **AWS Elastic Beanstalk** (PaaS) con base de datos **AWS RDS PostgreSQL**.

**URL del entorno:** `http://blacklist-env.eba-mscqmajg.us-east-1.elasticbeanstalk.com`

---

## Stack Tecnológico

| Tecnología | Versión | Rol |
|---|---|---|
| Python | 3.8 | Lenguaje base |
| Flask | 1.1.4 | Framework web |
| Flask-RESTful | 0.3.9 | Patrón REST orientado a objetos |
| Flask-SQLAlchemy | 2.5.1 | ORM para PostgreSQL |
| Flask-Marshmallow | 0.14.0 | Serialización y validación |
| Flask-JWT-Extended | 3.25.1 | Autenticación con Bearer Token |
| PostgreSQL | 14.x | Motor de base de datos (AWS RDS) |
| Gunicorn | 20.1.0 | Servidor WSGI de producción |

---

## Endpoints

### POST `/blacklists`
Agrega un email a la lista negra global.

**Headers:**
```
Authorization: Bearer <STATIC_TOKEN>
Content-Type: application/json
```

**Body:**
```json
{
  "email": "usuario@dominio.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Motivo opcional (máx 255 caracteres)"
}
```

**Respuestas:**
- `201 Created` – Email agregado exitosamente
- `400 Bad Request` – Datos inválidos o falta campo requerido
- `401 Unauthorized` – Token inválido o ausente
- `409 Conflict` – El email ya está en la lista negra

---

### GET `/blacklists/<email>`
Consulta si un email está en la lista negra.

**Headers:**
```
Authorization: Bearer <STATIC_TOKEN>
```

**Respuestas:**
- `200 OK` – `{"isBlacklisted": true, "blockedReason": "..."}`
- `200 OK` – `{"isBlacklisted": false, "blockedReason": null}`
- `401 Unauthorized` – Token inválido o ausente

---

### GET `/health`
Health check del servicio (usado por el Load Balancer de EB).

**Respuesta:** `{"status": "ok"}`

---

## Estructura del Proyecto

```
├── application.py          # Entry point de Elastic Beanstalk
├── requirements.txt        # Dependencias con versiones exactas
├── Procfile                # Comando de inicio: gunicorn
├── .gitignore
├── .ebextensions/
│   ├── 01_packages.config  # Paquetes yum del sistema
│   └── 02_environment.config # WSGIPath y health check path
└── app/
    ├── __init__.py         # App factory (create_app)
    ├── config.py           # Configuración desde variables de entorno
    ├── models.py           # Modelo BlacklistEntry (SQLAlchemy)
    ├── schemas.py          # Validación de entrada/salida (Marshmallow)
    └── views.py            # Recursos Flask-RESTful (POST y GET)
```

---

## Variables de Entorno (configuradas en EB, nunca en el repo)

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Connection string de PostgreSQL (RDS) |
| `STATIC_TOKEN` | Bearer token estático para autenticación |
| `JWT_SECRET_KEY` | Clave secreta para Flask-JWT-Extended |

---

## Ejecución Local

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
export DATABASE_URL="postgresql://user:pass@localhost:5432/blacklistdb"
export STATIC_TOKEN="mi-token-local"
export JWT_SECRET_KEY="mi-secreto-local"

# 4. Ejecutar
python application.py
```

---

## Infraestructura AWS

- **Elastic Beanstalk:** entorno `blacklist-env`, plataforma Python 3.8, Load Balanced
- **Auto Scaling:** mínimo 3 instancias, máximo 6 (t3.small)
- **RDS:** PostgreSQL 14, instancia db.t3.micro, VPC privada
- **Región:** us-east-1

---

## Colección Postman

La documentación completa de la API con escenarios de prueba está publicada en Postman:

> *(URL de la colección publicada — agregar después de publicar en Postman)*
