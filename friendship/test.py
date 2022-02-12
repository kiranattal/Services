import requests
import logging

from utils.config import filemode,filename,format,datefmt

logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)


BASE="http://127.0.0.1:5002"

#requests.post(BASE+"/friendshiprequest",data={"requested_by":"Kiran","requested_to":"Ninad"})

# print(requests.put(BASE+"/friendshiprequests/Friendship - c4c0a255-f8f2-489d-9b86-27a995177506",data={"requested_by":"Kiran","requested_to":"Ninad","status":"Unfriend"}).json())
# print(requests.get(BASE+"/friendshiprequests/Friendship - c4c0a255-f8f2-489d-9b86-27a995177506").json())


requests.post(BASE+"/friendshiprequest",data={"requested_by":"Kiran","requested_to":"Ninad"})

#print(requests.get(BASE+"/friendship/notification/Ninad").json())

#requests.put(BASE+"/friendship/notification/Ninad",data={"notification_id":"Notification - f482a34b-be9e-4864-8b28-9309cc758602","status":"Accepted","sender":"Kiran1","reciever":"Ninad1"})

print(requests.get(BASE+"/friends/Ninad").json())