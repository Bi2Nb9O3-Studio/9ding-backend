import base64
import requests

input("Start post img test")

url_postimg = "http://localhost:5000/api/post-image"
resp=requests.post(url_postimg,
              json={
                  "image": "data:image/png;base64,"+base64.b64encode(open("./Fox.png", "rb").read()).decode(),
                    "stu_name": "Mr.example",
                    "category": "example-category",
                    "work_name": "example-work",
                    "teacher": "Mr.example"
              })
print(resp.status_code,resp.json())