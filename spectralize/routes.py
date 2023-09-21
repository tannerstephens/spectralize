from flask import Blueprint, render_template, request, send_file

from spectralize.ghost_generator import GhostGenerator

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return render_template("home.html")


@routes.route("/gen")
def generate():
    generator = GhostGenerator()

    ghost = generator.generate_bytes(**request.args)

    return send_file(ghost, mimetype="image/png")
