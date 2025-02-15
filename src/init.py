
import auto_update as atp
import os
os.makedirs("./configs/", exist_ok=True)
os.makedirs("./logs/", exist_ok=True)
os.makedirs("./models/", exist_ok=True)
os.makedirs("./bundle/", exist_ok=True)
atp.download_font()
atp.update_bundle()
