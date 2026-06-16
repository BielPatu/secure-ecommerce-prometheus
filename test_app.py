import requests
import json

BASE_URL = "https://localhost:5000"

def test_register():
    data = {"username": "testuser", "password": "testpass"}
    resp = requests.post(BASE_URL + "/register", json=data, verify=False)
    print(f"Register: {resp.status_code} - {resp.json()}")
    return resp.json().get("mfa_secret")

def test_login(secret):
    import pyotp
    totp = pyotp.TOTP(secret)
    code = totp.now()
    data = {"username": "testuser", "password": "testpass", "code": code}
    resp = requests.post(BASE_URL + "/login", json=data, verify=False)
    print(f"Login: {resp.status_code} - {resp.json()}")
    return resp.json().get("token")

def test_products(token):
    headers = {"Authorization": f"Bearer {token}"}
    # Add product
    data = {"name": "Test Product", "price": "29.99"}
    resp = requests.post(BASE_URL + "/products", json=data, headers=headers, verify=False)
    print(f"Add Product: {resp.status_code} - {resp.json()}")
    # Get products
    resp = requests.get(BASE_URL + "/products", headers=headers, verify=False)
    print(f"Get Products: {resp.status_code} - {resp.json()}")

def test_metrics():
    resp = requests.get(BASE_URL + "/metrics", verify=False)
    print(f"Metrics: {resp.status_code}")
    print(resp.text[:500])  # First 500 chars

if __name__ == "__main__":
    print("Testing the secure e-commerce platform...")
    secret = test_register()
    if secret:
        token = test_login(secret)
        if token:
            test_products(token)
    test_metrics()
    print("Tests completed.")