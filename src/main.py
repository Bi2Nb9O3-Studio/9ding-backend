import os
import app
from database import db

db.init()
os.makedirs("./configs/",exist_ok=True)
os.makedirs("./logs/",exist_ok=True)
pic=app.Picture()
app.app.run(debug=True)