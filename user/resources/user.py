
from xmlrpc.client import boolean
from utils.config import filemode,filename,format,datefmt,project_id
from flask import request, Blueprint,make_response, jsonify
from flask_restful import Api, Resource, reqparse
from utils import database, utils
import logging
import uuid
from werkzeug.exceptions import abort
from google.cloud import pubsub_v1

# from app import app
user_bp = Blueprint("api", __name__)
user_api = Api(user_bp)


#user_api is to add resource, and blueprint object is passed as parameter
#blueprint obkect has all the routes that are then registered to real application
#resource, user_api ,blueprint object, real application(app)

logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)

    
user_args = reqparse.RequestParser()
user_args.add_argument('email', type=str, help='Email is mandatory',required=True)
user_args.add_argument('first_name',type=str)
user_args.add_argument('date_of_birth', type=str,required=False)
user_args.add_argument('number_of_friends',type=int,default=0)
user_args.add_argument('last_name',type=str)
user_args.add_argument('is_active',type=boolean)

posts_args=reqparse.RequestParser()
posts_args.add_argument('post_content',type=str,required=True,help="Mandatory")
posts_args.add_argument("creator",type=str,required=True,help="Mandatory")
posts_args.add_argument("is_visible",type=bool,required=False,help="Mandatory",default=True)

class users(Resource):
    def get(self):
        self.send_header('Content-Type', 'blabla' )

        self.end_headers()

        response={}
        user_docs=[]
        docs=database.user_collection.stream()
        for doc in docs:
            doc_dict=doc.to_dict()
            user_docs.append(doc_dict)
        response["data"]=user_docs
        return response

class user(Resource):


    def get(self,user_id):
        response={}
        user_doc={}
        docs=database.user_collection.stream()
        
        for doc in docs:
            user_doc=doc.to_dict()
            logging.info(user_id)
            logging.info(user_doc["user_id"])
            
            if user_doc["user_id"]==user_id:
                
                notifications=[]
                friendship_docs=database.user_collection.where(u"requested_to",u"==",user_doc["user_id"]).stream()
                for friendship_doc in friendship_docs:
                    friendship_doc_dict=friendship_doc.to_dict()
                    notifications.append(friendship_doc_dict["subscription"])
                user_doc.update({"notifications":notifications})
                response["data"]=user_doc
                return response
    
    def post(self):
        args = user_args.parse_args()
        doc_ref = database.user_collection.where(u'email',u'==',(args["email"]))
        docs = doc_ref.get()
        for any_doc in docs:
            logging.info(any_doc.to_dict())
            return {"error":"Already Exists"},400 # error handling part
        else:
            user_id= "User-" + str(uuid.uuid1())
            user_data=args
            user_data.update({"user_id":user_id})
            database.user_collection.document(user_id).set(user_data)
            
        
    def put(self,user_id):
        
        args=user_args.parse_args()
        doc_ref = database.user_collection.document(user_id) #reference to the document in FS
        logging.info(user_id)  # document object in key-value format
        if doc_ref.get().exists:  
                    database.user_collection.document(user_id).update(request.json)
                    #logging.info("Original doc : "+ doc_ref.get().to_dict()+" inserted with "+request.json+" fields"+"query is")  
                    
                    return 200
        else:
                    logging.error("Document doesnt exist"+args["email"])
                    #abort(404) # error handling part
                    return(not_found(404))
    
    def delete(self,user_id): 
        doc_ref=database.user_collection.document(user_id)
        if doc_ref.get().exists:
           is_active_data={"is_active":"False"}
           database.user_collection.document(user_id).update(is_active_data)
        else:
            return {"error":"Bad Request"}, 400


# class post_(Resource):
    # def post(self):
    #     response={}
    #     logging.info(request.json)
    #     args=posts_args.parse_args()
    #     post_id="Post - "+str(uuid.uuid1())
    #     post_doc=args
    #     created_on=utils.current_milli_time()
    #     post_doc.update({"created_on":created_on})
    #     post_doc.update({"modified_on":created_on})
    #     post_doc.update({"post_id":post_id})
    #     post_doc.update(request.json)
    #     database.post_collection.document(post_id).set(post_doc)
    #     response["data"]={"Added":"Post was created Successfuly"}
    #     return response

    # def get(self, post_id):
    #     response={}
    #     post_doc=database.post_collection.document(post_id).get().to_dict()
    #     if post_doc is not None:
    #         response["data"]=post_doc
    #         return response
    #     else:
    #         response["data"]={"error":"Not Present"}
    #         return response
    
    # def put(self, post_id):
    #     response={}  
    #     post_doc_ref=database.post_collection.document(post_id)
    #     if post_doc_ref.get().exists:
    #         args=posts_args.parse_args()
    #         final_post_doc=args
    #         final_post_doc.update(request.json)
    #         final_post_doc["modified_on"]=utils.current_milli_time()
    #         database.post_collection.document(post_id).update(final_post_doc)
    #         response["data"]={"Added":"Post was modified successfuly"}
    #     else:
    #         response["data"]={"error":"Post doesnt exist"}
    #     return response
    
    # def delete(self, post_id):
    #     response={}
    #     post_doc_ref=database.post_collection.document(post_id)
    #     if post_doc_ref.get().exists:
    #         visible_status={"is_visible":"False"}
    #         database.post_collection.document(post_id).update(visible_status)
    #         response["data"]={"Post":"Post was deleted successfully"}
    #     else:
    #         response["data"]={"Post":"Post was not found"}
    #     return response

@user_bp.errorhandler(404)
def not_found(error):
    logging.debug("Inside make_Response")
    return make_response(jsonify({"error":"The user to be modified was not Found"}),404)


user_api.add_resource(user,"/user","/user/<string:user_id>")
user_api.add_resource(users,"/users")
