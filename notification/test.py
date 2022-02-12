import requests
import logging

from utils.config import filemode,filename,format,datefmt

logging.basicConfig(filename=filename,filemode=filemode,format=format,datefmt=datefmt,level=logging.INFO)


BASE="http://127.0.0.1:5005"

#requests.post(BASE+"/friendshiprequest",data={"requested_by":"Kiran","requested_to":"Ninad"})

# print(requests.put(BASE+"/friendshiprequests/Friendship - c4c0a255-f8f2-489d-9b86-27a995177506",data={"requested_by":"Kiran","requested_to":"Ninad","status":"Unfriend"}).json())
# print(requests.get(BASE+"/friendshiprequests/Friendship - c4c0a255-f8f2-489d-9b86-27a995177506").json())


#requests.post(BASE+"/friendshiprequest",data={"requested_by":"Kiran","requested_to":"Ninad"})

print(requests.get(BASE+"/notifications/Kiran10").json())

#print(requests.put(BASE+"/notifications/Ninad",data={"notification_id":"Notification - 9afdf5e7-dcae-4f1b-9884-283f7b24a15d","status":"TestStatus","sender":"Kiran1","reciever":"Ninad"}).json())

#print(requests.get(BASE+"/friends/Ninad").json())