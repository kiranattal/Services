from google.cloud import firestore
from google.cloud import storage
from utils.config import project_id,user_collection_url,posts_collection_url
firestore_client=firestore.Client(project=project_id)
user_collection=firestore_client.collection(user_collection_url)
post_collection=firestore_client.collection(posts_collection_url)
