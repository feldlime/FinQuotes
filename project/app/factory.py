from typing import Optional

from flask import Flask


def create_app(config: Optional[object] = None) -> Flask:
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)

    return app
