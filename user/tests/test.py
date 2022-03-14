import requests

BASE="http://127.0.0.1:5000/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'ACCEPT-ENCODING' : 'gzip, deflate, br',
    'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'REFERER' : 'https://www.google.com/'
}

users=[
{"first_name":"Kiran","last_name":"Attal","email":"attal.kiran@gmail.com","date_of_birth":"250788","is_active":True},
{"first_name":"Ninad","last_name":"Sakhadev","email":"ninadsakhadev@gmail.com","date_of_birth":"230684","is_active":True},
{"first_name":"Cia","last_name":"Sakhadev","email":"ciasakhadev@gmail.com","date_of_birth":"281217","is_active":True},
{"first_name":"Myra","last_name":"Sakhadev","email":"myrasakhadev@gmail.com","date_of_birth":"281217","is_active":True}
]

# for one_user in users:
#     response=requests.post(BASE+"user",data=users[0])
#     print(response.json())

response=requests.get(BASE+"user/User-c187e1d0-8725-11ec-a8cf-1e00310cd079",allow_redirects=True,headers=headers)
print(response.json())

# response=requests.put(BASE+"/user/User-f8f190a0-8683-11ec-8657-1e00310cd05",json={"email":"kiran_attal@scmhrd.edu","last_name":"Attal","tags":["life","learning","swag"]})
# print(response.json())

# response=requests.delete(BASE+"/user/User-f8f190a0-8683-11ec-8657-1e00310cd078")
# print(response.json())
# # response=requests.get(BASE+"users")
# # print(response.json())

# files={"files": open("./uploads1/cia_myra.jpeg","rb")}
# response=requests.post(BASE+"/posts",files=files, data={"user_id":"123456"})
# print(response.json())

# new_files={"files": open("./uploads2/three_of_us.jpeg","rb")}
# response=requests.put(BASE+"/posts/Post - 1dad1f5f-bf48-4000-b1c3-2765a432dd82",files=new_files)
# response=requests.get(BASE+"/posts/Post - 1dad1f5f-bf48-4000-b1c3-2765a432dd82")
# print(response.json())

# response=requests.delete(BASE+"/posts/Post - f8546c5a-93c6-4f2d-bf08-8b9aee50aedf")
# print(response.json())

# response=requests.get(BASE+"/posts/Post - 1dad1f5f-bf48-4000-b1c3-2765a432dd82")
# print(response.json())
