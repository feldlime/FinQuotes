from project import create_app, Config

config = Config()
app = create_app(config)

if __name__ == '__main__':
    app.run(debug=app.debug)


