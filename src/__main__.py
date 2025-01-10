import os
import sys
import app.setup
import app.models.database as db

db.db.init()
os.makedirs("./configs/", exist_ok=True)
os.makedirs("./logs/", exist_ok=True)

if __name__ == "__main__":
    debug="--debug" in sys.argv
    app.setup.run(debug=debug)