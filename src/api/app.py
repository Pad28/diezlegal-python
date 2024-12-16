from flask import Flask
from routes import uploads_routes, contracts_routes
import os


UPLOAD_FOLDER = f"{os.path.dirname(os.path.abspath(__file__))}/../../database_files"

# Inicializar flask
def create_app():
    app = Flask(__name__)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # routes
    app.register_blueprint(uploads_routes.bp)
    app.register_blueprint(contracts_routes.bp)

    return app
