import base64
import requests

input("Start post img test")

url_postimg = "http://localhost:5000/api/content/new"
for i in range(15):
  resp=requests.post(url_postimg,
                json={
                    "image": "data:image/png;base64,"+base64.b64encode(open("./Fox.png", "rb").read()).decode(),
                      "stu_name": "Mr.example",
                      "category": "example-category",
                      "work_name": "example-work",
                      "teacher": "Mr.example"
                },
                cookies={
                  "username":"admin",
                  "verification": "e12605e909e93824f5ea39eaee1f921abf4e7783ad5c208f132116a3fcd04c7ad39d977837414790d42ecd351f59da887d7c41f1a62b5463475bf1c6dc1bd556"
                })
# resp=requests.post("http://localhost:5000/api/config",
#                    json={
#                      "changed":"a"
#                    }
# )
  print(resp.status_code,resp.text)
