from flask import Flask

from extensions import db, bcrypt, jwt, limiter

import logging
import os

app = Flask(__name__)

# CONFIG
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# INICIALIZAR EXTENSÕES
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
limiter.init_app(app)

# LOGS
logging.basicConfig(
    filename="logs/security.log",
    level=logging.INFO
)

# IMPORTAR APÓS INIT
from routes.auth import auth
from routes.products import products
from monitoramento.prometheus import REQUEST_COUNT
from models.user import User  # Importar modelo antes de create_all
app.register_blueprint(auth)
app.register_blueprint(products)

from prometheus_client import generate_latest

# CRIAR BANCO
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"msg": "API funcionando"}

if __name__ == "__main__":
    # Usar HTTPS com certificados gerados
    app.run(
        debug=True,
        ssl_context=("certs/cert.pem", "certs/key.pem"),
        host="0.0.0.0",
        port=5000
    )