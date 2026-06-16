import requests
import threading
import time
import random

# Simulação de ataques

BASE_URL = "https://localhost:5000"

def simulate_ddos():
    """Simular DDoS com muitas requisições"""
    while True:
        try:
            requests.get(BASE_URL + "/", verify=False)
        except:
            pass
        time.sleep(0.01)  # Rápido

def simulate_brute_force():
    """Simular brute force no login"""
    usernames = ["admin", "user", "test"]
    passwords = ["123456", "password", "admin"]
    for _ in range(100):
        data = {
            "username": random.choice(usernames),
            "password": random.choice(passwords),
            "code": "000000"  # Código inválido
        }
        try:
            requests.post(BASE_URL + "/login", json=data, verify=False)
        except:
            pass
        time.sleep(0.1)

def simulate_intrusion():
    """Simular tentativa de acesso não autorizado"""
    # Tentar acessar produtos sem token
    try:
        resp = requests.get(BASE_URL + "/products", verify=False)
        print(f"Intrusion attempt: {resp.status_code}")
    except:
        pass

if __name__ == "__main__":
    print("Iniciando simulação de ataques...")

    # DDoS threads
    for _ in range(10):
        threading.Thread(target=simulate_ddos, daemon=True).start()

    # Brute force
    threading.Thread(target=simulate_brute_force, daemon=True).start()

    # Intrusion
    simulate_intrusion()

    # Manter rodando
    while True:
        time.sleep(1)