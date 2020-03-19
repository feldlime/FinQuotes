from pathlib import Path

from environs import Env

env: Env = Env()


ENV = env.str('ENV', 'production')
DEBUG = env.bool('DEBUG', False)
TESTING = env.bool('TESTING', False)

HOST = env.str('HOST', '0.0.0.0')
PORT = env.int('PORT', '8080')
BIND = f'{HOST}:{PORT}'

PROJECT_DIR = Path(__file__).parent
