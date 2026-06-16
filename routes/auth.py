from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models.user import User
from flask_jwt_extended import create_access_token
import pyotp
import logging
from monitoramento.prometheus import REQUEST_COUNT, FAILED_LOGIN_ATTEMPTS

auth = Blueprint("auth", __name__)

logger = logging.getLogger(__name__)

# REGISTER
@auth.route("/register", methods=["POST"])
def register():
    REQUEST_COUNT.labels(method='POST', endpoint='/register', status='200').inc()
    data = request.json

    hashed = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    secret = pyotp.random_base32()

    user = User(
        username=data["username"],
        password=hashed,
        mfa_secret=secret
    )

    db.session.add(user)
    db.session.commit()

    logger.info(f"Usuário {data['username']} registrado.")
    return jsonify({
        "msg": "Usuário criado",
        "mfa_secret": secret
    })

# LOGIN
@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(
        username=data["username"]
    ).first()

    if not user:
        FAILED_LOGIN_ATTEMPTS.inc()
        logger.warning(f"Tentativa de login com usuário inválido: {data['username']}")
        REQUEST_COUNT.labels(method='POST', endpoint='/login', status='401').inc()
        return jsonify({"msg": "Usuário inválido"}), 401

    if not bcrypt.check_password_hash(
        user.password,
        data["password"]
    ):
        FAILED_LOGIN_ATTEMPTS.inc()
        logger.warning(f"Tentativa de login com senha inválida para usuário: {data['username']}")
        REQUEST_COUNT.labels(method='POST', endpoint='/login', status='401').inc()
        return jsonify({"msg": "Senha inválida"}), 401

    totp = pyotp.TOTP(user.mfa_secret)

    if not totp.verify(data["code"]):
        FAILED_LOGIN_ATTEMPTS.inc()
        logger.warning(f"Código MFA inválido para usuário: {data['username']}")
        REQUEST_COUNT.labels(method='POST', endpoint='/login', status='401').inc()
        return jsonify({"msg": "Código MFA inválido"}), 401

    token = create_access_token(identity=user.username)
    REQUEST_COUNT.labels(method='POST', endpoint='/login', status='200').inc()
    logger.info(f"Login bem-sucedido para usuário: {data['username']}")
    return jsonify({"token": token})