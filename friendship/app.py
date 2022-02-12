
from flask import Flask, Blueprint
from flask_restful import Api
from resources.friendship import friendship_bp

app= Flask(__name__)
app.register_blueprint(friendship_bp)

if __name__=="__main__":
    app.run(port=5002)
