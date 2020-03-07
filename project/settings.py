from pathlib import Path

from environs import Env

__all__ = (
    'env',
)

env: Env = Env()

HOST = env.str('HOST', '0.0.0.0')
PORT = env.int('PORT', '8080')

BIND = f'{HOST}:{PORT}'

PROJECT_DIR = Path(__file__).parent

