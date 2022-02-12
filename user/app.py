from utils.config import filemode,filename,format,datefmt

from flask import Flask
import logging
#import redis

from resources.user import user_bp


logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)

app=Flask(__name__) 
app.register_blueprint(user_bp)

if __name__ == "__main__":
    logging.info("Running user app")
    app.run(port=5000)

