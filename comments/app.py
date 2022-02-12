from flask import Flask
from resources.comments import comments_bp
import logging,os
from utils.config import filename,filemode,datefmt,format,credentials_path

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= credentials_path

app=Flask(__name__)
app.register_blueprint(comments_bp)

logging.basicConfig(filename=filename, filemode=filemode, format=format,datefmt=datefmt)


if __name__=="__main__":
    logging.info("Running comments app on 5003")
    app.run(port=5004)

