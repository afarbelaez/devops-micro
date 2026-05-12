# New Relic se inicializa vía newrelic-admin run-program en el CMD del Dockerfile
from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(debug=False)
