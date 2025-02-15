import auto_update as atp
import os
import app.setup

if __name__ == "__main__":
    os.makedirs("./models/", exist_ok=True)
    atp.download_font()
    atp.update_bundle()
    app.setup.create_app().run(port=5002)