import newrelic.agent
newrelic.agent.initialize()   # Lee NEW_RELIC_LICENSE_KEY y NEW_RELIC_APP_NAME del entorno

from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(debug=False)
