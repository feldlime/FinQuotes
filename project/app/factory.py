from typing import Optional

from flask import Flask

from .api import bp


def create_app(config: Optional[object] = None) -> Flask:
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)

    app.register_blueprint(bp, url_prefix='/api')

    return app
