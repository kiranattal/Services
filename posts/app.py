from utils.config import filemode,filename,format,datefmt

from flask import Flask
import logging
#import redis


from resources.posts import posts_bp

logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)

app=Flask(__name__) 

app.register_blueprint(posts_bp)
#cache = redis.Redis(host='redis', port=6379)
if __name__ == "__main__":
    app.run(port=5001)

