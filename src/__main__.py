import app.models.database as db
db.db.init()
import os
os.makedirs("./configs/", exist_ok=True)
os.makedirs("./logs/", exist_ok=True)
os.makedirs("./models/", exist_ok=True)
import sys
import app.setup
import app.auth
if __name__ == "__main__":
    debug="--debug" in sys.argv
    app.setup.run(debug=debug)