from google.cloud import firestore
from utils.config import project_id,comments_collection_url
firestore_client=firestore.Client(project=project_id)
comments_collection=firestore_client.collection(comments_collection_url)