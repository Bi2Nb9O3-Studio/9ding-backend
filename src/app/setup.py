from flask import Flask
from . import routes

app=Flask(__name__)
app.register_blueprint(routes.built_blueprint)

def run(debug):
    app.run(debug=debug)
