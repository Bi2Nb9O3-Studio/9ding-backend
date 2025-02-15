import auto_update as atp
import os

os.makedirs("./models/", exist_ok=True)
atp.download_font()
atp.update_bundle()
