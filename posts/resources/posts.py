
from cmath import log
from http.client import responses
import uuid, traceback
from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse

from utils.config import bucket_name, filemode,filename,format,datefmt,project_id
from utils import utils
import logging, datetime
from google.cloud import storage, pubsub_v1
from utils import database




logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)


posts_bp=Blueprint("post-api",__name__)
posts_api=Api(posts_bp)

post_args=reqparse.RequestParser()
post_args.add_argument("created_by",type=str)
post_args.add_argument("post_description",type=str)
post_args.add_argument("is_visible",type=bool)

def delete_file_from_gcp(bucket_name, folder_name, file_name):
    #Deletes blob from the bucket
    try:
        storage_client=storage.Client()
        bucket=storage_client.bucket(bucket_name)
        current_path=folder_name+"/"+file_name
        blob=bucket.blob(current_path)
        logging.info(bucket_name)
        logging.info(current_path)
        if storage.Blob(bucket=bucket,name=current_path).exists(storage_client):
            blob.delete()
            print("Blob deleted",f"{bucket_name}+{current_path}")
    
    except Exception as e:
        logging.error(traceback.format_exc())
    
def replace_file_from_gcp(bucket_name, folder_name, file_name,new_files):
    delete_file_from_gcp(bucket_name,folder_name,file_name)#delete existing file
    try: #uploading new_file
        new_data_to_upload=new_files[0].read()
        storage_client=storage.Client()
        bucket=storage_client.bucket(bucket_name)
        path=folder_name+"/"+file_name # path remains same, created_by and post_id as folder and file name respectively
        blob=storage.Blob(bucket=bucket,name=path)
        blob.upload_from_string(new_data_to_upload,"image/jpeg")

    except Exception as e:
        logging.error(traceback.format_exc())


       
class Post(Resource):
    def post(self):
        response={}
        args=post_args.parse_args()
        logging.info(args)
        logging.info("This was args")
        #uploadig file in gcp
        files =request.files.getlist('files')
        post_id="Post-"+f"{uuid.uuid4()}"
        data_to_upload=files[0].read()
        storage_client=storage.Client()
        bucket=storage_client.bucket(bucket_name)
        folder_name=f"{args['created_by']}"
        file_name= post_id
        destination_path=f"{folder_name}/{file_name}"
        logging.info(destination_path)
        try:
            blob = storage.Blob(bucket=bucket,name=destination_path)
            blob.upload_from_string(data_to_upload,"image/jpeg") 
            logging.info("Pic is getting uploaded")
        except Exception as e:
            logging.error("Error in uploading file, in POST request")
   
        post_doc=args
        created_on=utils.current_milli_time()
        post_doc.update({"created_on":created_on})
        post_doc.update({"modified_on":created_on}) #created on and modified on is same when post is created
        post_doc.update({"post_id":post_id})
        post_doc.update({"gcp_location":f"{bucket.name}/{destination_path}"})
        logging.info(post_doc)
        logging.info("This is post doc")
        database.post_collection.document(post_id).set(post_doc)
            #Create a topic in pubsub for this post and subscribe the post creator to it
        try:
                publisher = pubsub_v1.PublisherClient()
                topic_id=post_id.replace(" ","")
                topic_path = publisher.topic_path(project_id, topic_id)

                publisher.create_topic(request={"name": topic_path})
                subscriber=pubsub_v1.SubscriberClient()
                subscription_id=str(args["created_by"])
                logging.info(subscription_id)
                subscription_path = subscriber.subscription_path(project_id, subscription_id)
                with subscriber:
                     subscriber.create_subscription(
                        request={"name": subscription_path, "topic": topic_path}
                    )


                
                response["data"]={"Added":"Post was created Successfuly"}
        except Exception as e:
                logging.error(e)
        return response
    
    def get(self):
        posts=[]
        response={}
        args=post_args.parse_args()
        posts=database.post_collection.where(u"created_by",u"==",args["created_by"]).stream()
        for post in posts:
            post_doc=post.to_dict()
            posts.append(post_doc)
        response["data"]=posts
        return response

        
class Posts(Resource):
    def put(self,post_id):
        args=post_args.parse_args()
        logging.info(args)
        post_doc_ref=database.post_collection.document(post_id)
        post_doc=post_doc_ref.get()
        logging.info(post_doc_ref)
        logging.info(post_doc)
        if post_doc.exists:
            post_data=post_doc.to_dict()
            logging.info(post_data)
            files =request.files.getlist('files')
            if files is not None:
                post_current_path=post_data["gcp_location"].split("/")
                folder_name=post_current_path[1]
                file_name=post_current_path[-1]
                bucket_name=post_current_path[0]
                logging.info(bucket_name)
                logging.info(folder_name)
                logging.info(file_name)
                #Delete the existing file with file_name in bucket_name/folder_name
                #Insert the new file in location bucket_name/folder_name with file_name
                replace_file_from_gcp(bucket_name,folder_name,file_name,files)
                return {"Successful":"Successful Updation"}
            else:
                return {"Error":"Document for updation doesnt exist"}


    def get(self, post_id):
        args=post_args.parse_args()
        response={}

        post_doc_ref=database.post_collection.document(post_id)
        post_doc=post_doc_ref.get()
        if post_doc.exists:
            post_data=post_doc.to_dict()
            gcp_path=post_data["gcp_location"].split("/")
            file_path_in_bucket=f"{gcp_path[1]}"+"/"f"{gcp_path[2]}"    #buckername+foldername+filename, taking last 2 portions to make destination path in the bucket
            url=generate_download_signed_url_v4(bucket_name,file_path_in_bucket)
            post_data.update({"url":url})
            response["data"]=post_data
            return response
        else:
            response["data"]={"Error":"Document doesnt exist"}
            return response

    def delete(self, post_id):
        response={}
        args=post_args.parse_args()
        post_doc_ref=database.post_collection.document(post_id)
        post_doc=post_doc_ref.get()
        if post_doc.exists:
            post_data=post_doc.to_dict()
            gcp_path=post_data["gcp_location"]
            folders=gcp_path.split("/")
            folder_name=folders[1]
            file_name=folders[-1]
            logging.info(folder_name)
            logging.info(file_name)
            delete_file_from_gcp(bucket_name,folder_name,file_name)
            try:
                #post_doc_ref.delete()
                response["data"]={"successful":"Successful Deletion"}
            except Exception as e:
                logging.error("Error in deleting post from Firestore")
                response["data"]= {"error":"Error in deleting post from Firestore"}
            return response
        else:
            response["data"]={"Error":"Document doesnt exist"}
            return response






        
def generate_download_signed_url_v4(bucket_name,file_path_in_bucket):
    storage_client=storage.Client()
    bucket=storage_client.bucket(bucket_name)
    blob=bucket.blob(file_path_in_bucket)
    url=blob.generate_signed_url( version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(days=7), #max expiration time
        # Allow GET requests using this URL.
        method="GET")
    return url



posts_api.add_resource(Post,"/post")
posts_api.add_resource(Posts,"/posts/<string:post_id>")


