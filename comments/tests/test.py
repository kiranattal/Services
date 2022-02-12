import requests

BASE="http://127.0.0.1:5004"

#print(requests.get(BASE+"/comment/1234").json())
print(requests.post(BASE+"/comment/Post-60564ae1-e4a7-4af7-bebb-9523b1be97c4",data={"created_by":"Kiran12","comment_description":"This is test commentnew_again"}).json())

# print(requests.get(BASE+"/comment/1234").json())

# print(requests.put(BASE+"/comment/1234").json())
# print(requests.delete(BASE+"/comment/1234").json())

