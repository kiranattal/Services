
from flask import Flask, Blueprint
from flask_restful import Api
from resources. notification import notification_bp

app= Flask(__name__)
app.register_blueprint(notification_bp)

if __name__=="__main__":
    app.run(port=5005)
