# Plataforma de E-commerce Segura

Projeto de protótipo de plataforma de e-commerce com foco em segurança, implementado em Python com Flask.

A aplicação demonstra uma API segura com autenticação multifatorial, criptografia de dados, HTTPS local, mitigação de abuso e monitoramento de métricas.

## Recursos Principais

- Registro e login com **JWT**
- Autenticação multifatorial **MFA** via **TOTP**
- Criptografia de dados em repouso com **Fernet AES**
- HTTPS local usando certificados autoassinados
- Rate limiting para mitigação de abuso e DDoS
- Monitoramento com métricas **Prometheus**
- Logs de segurança em `logs/security.log`

## Tecnologias

- Python 3.11+ / 3.12+ recomendado
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Limiter
- cryptography
- pyotp
- prometheus_client

## Requisitos

- Python 3.11 ou superior
- `pip`
- Permissões para criar arquivos em `certs/` e `logs/`

## Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Gere os certificados SSL para rodar em HTTPS localmente:

```bash
python generate_cert.py
```

3. Configure variáveis de ambiente opcionais:

- `SECRET_KEY` – chave do Flask
- `JWT_SECRET_KEY` – chave para geração de JWT
- `DATABASE_URI` – URI do banco de dados (padrão: `sqlite:///database.db`)
- `ENCRYPTION_KEY` – chave para criptografia Fernet (se não definida, gera uma nova chave temporária)

4. Inicie a aplicação:

```bash
python app.py
```

A API estará disponível em:

```text
https://localhost:5000
```

> Em ambiente de desenvolvimento local, use `--insecure` com `curl` para ignorar o certificado autoassinado.

## Endpoints

### GET /
Retorna um status simples de funcionamento.

### POST /register
Registra um usuário e retorna o segredo MFA.

Exemplo:

```bash
curl -X POST https://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}' --insecure
```

### POST /login
Faz login com senha e código MFA. Retorna token JWT.

Exemplo:

```bash
curl -X POST https://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass","code":"123456"}' --insecure
```

### GET /products
Lista produtos protegidos por JWT.

Exemplo:

```bash
curl -X GET https://localhost:5000/products \
  -H "Authorization: Bearer <token>" --insecure
```

### POST /products
Adiciona um produto com dados criptografados.

Exemplo:

```bash
curl -X POST https://localhost:5000/products \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Produto","price":"10.00"}' --insecure
```

### GET /metrics
Expõe métricas Prometheus.

Exemplo:

```bash
curl https://localhost:5000/metrics --insecure
```

## Estrutura do Projeto

- `app.py` – ponto de entrada da aplicação
- `extensions.py` – inicialização de extensões Flask
- `generate_cert.py` – gera certificados TLS autoassinados
- `routes/auth.py` – rotas de autenticação e MFA
- `routes/products.py` – rotas de produtos com criptografia e rate limiting
- `models/user.py` – modelo de usuário
- `security/encryption.py` – criptografia Fernet para dados sensíveis
- `monitoramento/prometheus.py` – métricas de monitoramento
- `simulate_attacks.py` – simulação de ataques para testes
- `requirements.txt` – dependências do projeto
- `certs/` – certificados TLS locais
- `logs/` – logs de segurança

## Segurança e Considerações

- O projeto usa **HTTPS local** com certificados autoassinados apenas para desenvolvimento.
- O segredo MFA é gerado no registro e deve ser armazenado com segurança no cliente.
- `ENCRYPTION_KEY` deve ser configurado para manter a criptografia de dados persistente.
- Em produção, substitua os certificados autoassinados e utilize um armazenamento seguro para chaves.

## Testes e Simulações

- Execute `python simulate_attacks.py` para acionar cenários de ataque simulados.
- Verifique o arquivo `logs/security.log` para eventos de autenticação e segurança.
- Inspecione `/metrics` para métricas de requisição, tempo de resposta e falhas.

## Observações

Este repositório é um exemplo de arquitetura de segurança para APIs. Ajustes adicionais são necessários antes de usar em produção, especialmente em relação a armazenamento de chaves, certificados e validação de entrada.
"# secure-ecommerce-prometheus" 
