from calendar import c
from dataclasses import dataclass

from flask import Flask, Blueprint, jsonify, make_response
from flask_restful import Api, reqparse, Resource
import logging,uuid
from utils.config import filename,filemode,datefmt,format, project_id
from utils import database
from google.cloud import pubsub_v1
from concurrent import futures

comments_bp=Blueprint("api",__name__)
api=Api(comments_bp)


logging.basicConfig(filename=filename, filemode=filemode, format=format,datefmt=datefmt)


comments_args=reqparse.RequestParser()
comments_args.add_argument("post_id",type=str)
comments_args.add_argument("created_by",type=str, required=True)
comments_args.add_argument("comment_description",type=str, required=True)

class Comment(Resource):
    def post(self,post_id):
        args=comments_args.parse_args()
        comment_doc=dict()
        comment_doc.update({"post_id":post_id})
        comment_doc.update({"created_by":args["created_by"]})
        comment_doc.update({"comment_description":args["comment_description"]})
        comment_id="Comment-"+str(uuid.uuid4())
        comment_doc.update({"comment_id":comment_id})
        publisher=pubsub_v1.PublisherClient()
      
        topic_id=post_id.replace(" ","")
        topic_path=publisher.topic_path(project_id,topic_id)
        comments=database.comments_collection.where(u"created_by",u"==",args["created_by"]).stream()
        number_of_comments=0
        for comment in comments:
            number_of_comments+=1
        if number_of_comments==0:
            subscriber=pubsub_v1.SubscriberClient()
            subscriber_id=args["created_by"].replace(" ","")
            subscription_path=subscriber.subscription_path(project_id,subscriber_id)
            comment_doc.update({"subscription_path":subscription_path})
            logging.info(subscription_path)
            
            with subscriber:
                subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}

            )
            
       
        publish_futures = []
        data = "For Post " + args["post_id"]+" commented by "+ args["created_by"]+" :"+args["comment_description"]
        data=data.encode("utf-8")
        future = publisher.publish(topic_path, data)
        print(future.result())

        print(f"Published messages to {topic_path}.")


# Wait for all the publish futures to resolve before exiting.
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

       
        database.comments_collection.document(comment_id).set(comment_doc)
            
    
    

class Comments(Resource):
    def get(self, comment_id):
        return {"comment_id_get":"comment_id_get"}
    def put(self, comment_id):
        return {"comment_id_put":"comment_id_put"}
    def delete(self, comment_id):
        return {"comment_id_delete":"comment_id_delete"}
    def get(self):
        return {"Get all comments":"Get All comments"}


api.add_resource(Comments,"/comments/<string:comment_id>")
api.add_resource(Comment,"/comment/<string:post_id>")
