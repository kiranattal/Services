
from cmath import log
from heapq import merge
from http.client import responses
import json
import logging
from google.cloud  import firestore

from utils.config import filemode,filename,format,datefmt,project_id
from flask import Flask, Blueprint, jsonify,make_response, abort
from flask_restful import Api, reqparse, Resource
from utils import database, utils
import uuid



friendship_bp=Blueprint("api",__name__)
api=Api(friendship_bp)

friendship_args=reqparse.RequestParser()
friendship_args.add_argument("requested_by",type=str,required=True)
friendship_args.add_argument("requested_to",type=str,required=True)
friendship_args.add_argument("status")
friendship_args.add_argument("requested_on")



logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)


class Friends(Resource):

    def get(self,user_id):
        friends=[]
        user_doc=database.friends.document(user_id).get().to_dict()
        friends=user_doc.get("friends")
        return make_response(jsonify(friends),200)

        #friends=database.friendship_collection.where(u"user_id",u)
        

class FriendshipRequest(Resource):
    def post(self):
        args=friendship_args.parse_args()
        logging.info(args)
        friendship_id="Friendship-"+ f"{uuid.uuid4()}"
        status="Requested"
        friendship_doc=args
        
        requested_on=utils.current_milli_time()
        modified_on=utils.current_milli_time() #Friendship request will have same created on and modified on
        friendship_doc.update({"status":status})
        friendship_doc.update({"requested_on":requested_on})
        friendship_doc.update({"modified_on":modified_on})
        friendship_doc.update({"friendship_id":friendship_id})
      
        #inserting new document in friendship collection in "friendship" database

        database.friendship_collection.document(friendship_id).set(friendship_doc)
        # inserting new document in notification_reciever collection
        notification=dict()
        notification_id= "Notification - " + str(uuid.uuid4())
        notification.update({"friendship_id":friendship_id})
        notification.update({"reciever":args["requested_to"]})
        notification.update({"sender":args["requested_by"]})
        notification.update({"notification_status":"unread"})
        notification.update({"notification_id":notification_id})
        notification.update({"triggered_at":requested_on})
        notification.update({"status":status})
        database.friendship_notification.document(notification_id).set(notification)


# class Notification(Resource):

#     def get(self,reciever):
#         response={}
#         notifications=[]
#         notification_docs=database.notification.where(u"reciever",u"==",reciever).where(u"status",u'==',"Requested").stream()
#         for doc in notification_docs:
#             notification_doc=doc.to_dict()
#             notifications.append(notification_doc)
#         notifications.sort(key=lambda x:int(x.get("triggered_at")),reverse=True)
#         response["data"]=notifications
#         return make_response(jsonify(response["data"]),200)

#     def put(self, reciever):
        
#         args=notification_args.parse_args()
#         notification_id=args["notification_id"]
#         logging.error(notification_id)
#         try:
#             database.notification.document(notification_id).update({"status":args["status"]})
#             database.notification.document(notification_id).update({"notification_status":"read"})
#             if(args["status"]=="Accepted"):
#                 if database.friends.document(reciever).get().exists:
#                    database.friends.document(reciever).update({u"friends":firestore.ArrayUnion([args['sender']])})
               
#                 else:
#                     database.friends.document(reciever).set({u"friends":[args["sender"]]})
#                 if database.friends.document(args["sender"]).get().exists:
#                     database.friends.document(args["sender"]).update({u"friends":firestore.ArrayUnion([args['reciever']])})
#                 else:
#                     database.friends.document(args["sender"]).set({u"friends":[args["reciever"]]})
#             return make_response({"Notification":"Updated"},200)
#         except Exception as e:
#             logging.error(e)
#             return not_found(404)
            
        





@friendship_bp.errorhandler(404)
def not_found(error):
    logging.debug("Inside make_Response")
    return make_response(jsonify({"error":"The user to be modified was not Found"}),404)
   
api.add_resource(Friends,"/friends/<string:user_id>")
api.add_resource(FriendshipRequest,"/friendshiprequest")



