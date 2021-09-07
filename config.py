import os

ZONE = 'test.arpa.'
DNS_SERV = '127.0.0.1'
TTL = 5
SECRET_KEY = os.environ.get('SECRET_KEY') or 'Li1upae4ohl8cudoohahx8EuT1ke4bai9Uthu2kei2ayooj5IeghooQuaephae1e'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

connection_options = { 
    'host': '192.168.99.91',
    'auth_username': 'bot',
    'auth_password': 'Bot12345!',
    'auth_strict_key': False, 
    'ssh_config_file': True, 
}   
