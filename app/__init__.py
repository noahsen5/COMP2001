# Initialize Flask app


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_pyfile('../config.py')

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
