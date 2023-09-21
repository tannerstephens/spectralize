from flask import Flask

from .routes import routes


class App(Flask):
    def __init__(self, config="spectralize.config.Config"):
        super().__init__(__name__)
        self.config.from_object(config)
        self.register_routes()

    def register_routes(self):
        self.register_blueprint(routes)

    def dev_server(self):
        self.run(debug=True, threaded=True, host="0.0.0.0", port=8000)
