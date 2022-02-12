
from cmath import log
from heapq import merge
from http.client import responses
import json
import logging
from google.cloud  import firestore, pubsub_v1


from utils.config import filemode,filename,format,datefmt,project_id,NUM_MESSAGES
from flask import Flask, Blueprint, jsonify,make_response, abort
from flask_restful import Api, reqparse, Resource
from utils import database, utils
import uuid
from google.api_core import retry



subscriber=pubsub_v1.SubscriberClient()
timeout=5
notification_bp=Blueprint("api",__name__)
api=Api(notification_bp)


friends_notification_args=reqparse.RequestParser()
friends_notification_args.add_argument("reciever",type=str,required=True)
friends_notification_args.add_argument("notification_id",type=str,required=True)
friends_notification_args.add_argument("sender",type=str,required=True)
friends_notification_args.add_argument("status",type=str,required=True)


logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()
   

  

class Notification(Resource):

    def get(self,reciever):
        response={}
        #First get all friend requests 
        friendship_notifications=[]
        notification_docs=database.friendship_notification.where(u"reciever",u"==",reciever).where(u"status",u'==',"Requested").stream()
        for doc in notification_docs:
            notification_doc=doc.to_dict()
            friendship_notifications.append(notification_doc)
        friendship_notifications.sort(key=lambda x:int(x.get("triggered_at")),reverse=True)
        #response["data"]["friendship"]=friendship_notifications
        #Now get all notification for posts where reciever has commented
        comment_notifications=[]
        
 
        subscription_path = subscriber.subscription_path(project_id, reciever)



        
        print(f"Listening for messages on {subscription_path}..\n")

       
       
       
        pub_sub_response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
                retry=retry.Retry(deadline=300),
            )
        ack_ids = []
        if pub_sub_response.received_messages:
                for received_message in pub_sub_response.received_messages:
                    print(f"Received: {received_message.message}")
                    message=str(received_message.message.data)
                    publish_time=str(received_message.message.publish_time)
                    comment_notification=dict()
                    comment_notification={"message":message,"publish_time":publish_time}
                    comment_notifications.append(comment_notification)
                    logging.info(comment_notification)
       
                    # data = received_message.message.data
                    # attributes = received_message.message.attributes
                    # message_id = received_message.message.message_id
                    # publish_time = received_message.message.publish_time
                    # print(data)
                    # print(attributes)
                    # print(message_id)
                    # print(publish_time)
                   
                    ack_ids.append(received_message.ack_id)
                    subscriber.acknowledge(
                            request={"subscription": subscription_path, "ack_ids": ack_ids}
                    )
        print(
            f"Received and acknowledged {len(pub_sub_response.received_messages)} messages from {subscription_path}."
             )
   
        response["friendship"]={"Friendship Requests":friendship_notifications}       
        response["comments"]={"Comment Updates on Posts":comment_notifications}
        return response

    def put(self, reciever):
        
        args=friends_notification_args.parse_args()
        notification_id=args["notification_id"]
        logging.info(notification_id)
        try:
            database.friendship_notification.document(notification_id).update({"status":args["status"]})
            database.friendship_notification.document(notification_id).update({"notification_status":"read"})
            if(args["status"]=="Accepted"):
                if database.friends.document(reciever).get().exists:
                   database.friends.document(reciever).update({u"friends":firestore.ArrayUnion([args['sender']])})
               
                else:
                    database.friends.document(reciever).set({u"friends":[args["sender"]]})
                if  database.friends.document(args["sender"]).get().exists:
                    database.friends.document(args["sender"]).update({u"friends":firestore.ArrayUnion([args['reciever']])})
                else:
                    database.friends.document(args["sender"]).set({u"friends":[args["reciever"]]})
            return make_response({"Notification":"Updated"},200)
        except Exception as e:
            logging.error(e)
            return not_found(404)
            
        





@notification_bp.errorhandler(404)
def not_found(error):
    logging.debug("Inside make_Response")
    return make_response(jsonify({"error":"The user to be modified was not Found"}),404)
   

api.add_resource(Notification,"/notifications/<string:reciever>")




