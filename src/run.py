import auto_update as atp
import os
os.makedirs("./models/", exist_ok=True)
atp.download_font()
atp.update_bundle()
import app.setup

if __name__ == "__main__":
    app.setup.create_app().run(port=5001)