from flask import Flask

from routes import validate, credit, transaction


def create_app():
    app = Flask(__name__)
    app.register_blueprint(validate.bp)
    app.register_blueprint(credit.bp)
    app.register_blueprint(transaction.bp)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
