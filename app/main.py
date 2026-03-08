from flask import Flask
from flask_cors import CORS

from routes import validate, credit, transaction
from routes import account, balance, subscription, notification, command


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(validate.bp)
    app.register_blueprint(credit.bp)
    app.register_blueprint(transaction.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(balance.bp)
    app.register_blueprint(subscription.bp)
    app.register_blueprint(notification.bp)
    app.register_blueprint(command.bp)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
