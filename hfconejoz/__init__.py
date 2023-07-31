from flask import Flask

def create_app():
    main = Flask(__name__)

    from .main import main as main_blueprint
    main.register_blueprint(main_blueprint)

    return main
