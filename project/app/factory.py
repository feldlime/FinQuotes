from flask import Flask


def create_app(config: object) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    # app.router.add

    return app
