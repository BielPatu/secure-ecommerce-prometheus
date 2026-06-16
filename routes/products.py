from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import limiter
from security.encryption import encrypt_data, decrypt_data
from monitoramento.prometheus import REQUEST_COUNT

products = Blueprint("products", __name__)

# Simular produtos (em produção, seria um modelo DB)
products_data = []

from monitoramento.prometheus import REQUEST_COUNT, RESPONSE_TIME
import time

@products.route("/products", methods=["GET"])
@jwt_required()
@limiter.limit("10 per minute")
def get_products():
    start = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/products', status='200').inc()
    # Descriptografar dados antes de retornar
    decrypted_products = []
    for prod in products_data:
        decrypted = {
            "name": decrypt_data(prod["name"]),
            "price": decrypt_data(prod["price"])
        }
        decrypted_products.append(decrypted)
    RESPONSE_TIME.labels(method='GET', endpoint='/products').observe(time.time() - start)
    return jsonify(decrypted_products)

@products.route("/products", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def add_product():
    start = time.time()
    REQUEST_COUNT.labels(method='POST', endpoint='/products', status='200').inc()
    data = request.json
    # Criptografar dados antes de armazenar
    encrypted_product = {
        "name": encrypt_data(data["name"]),
        "price": encrypt_data(str(data["price"]))
    }
    products_data.append(encrypted_product)
    RESPONSE_TIME.labels(method='POST', endpoint='/products').observe(time.time() - start)
    return jsonify({"msg": "Produto adicionado"})