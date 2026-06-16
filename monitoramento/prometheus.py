from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total App Requests',
    ['method', 'endpoint', 'status']
)

FAILED_LOGIN_ATTEMPTS = Counter(
    'failed_login_attempts_total',
    'Total Failed Login Attempts'
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of Active Users'
)

RESPONSE_TIME = Histogram(
    'response_time_seconds',
    'Response Time in Seconds',
    ['method', 'endpoint']
)