from flask import Flask

from .routes import routes


class App:
    def __init__(self, config="spectralize.config.Config"):
        self.app = Flask(__name__)
        self.app.config.from_object(config)
        self.register_routes()

    def register_routes(self):
        self.app.register_blueprint(routes)

    def dev_server(self):
        self.app.run(debug=True, threaded=True, host="0.0.0.0", port=8000)
