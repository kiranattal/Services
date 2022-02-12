import requests

BASE="http://127.0.0.1:5000/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'ACCEPT-ENCODING' : 'gzip, deflate, br',
    'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'REFERER' : 'https://www.google.com/'
}

# for one_user in users:
#response=requests.post(BASE+"user",data=users[0])
    #print(response.json())

response=requests.get(BASE+"user/Ninad",allow_redirects=True,headers=headers)
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
