import json
import auto_update as atp
import os

os.makedirs("./models/", exist_ok=True)
atp.download_font()
atp.update_bundle()
with open("./security.cfg","w",encoding="utf-8") as f:
    f.write(json.dumps({
        "salt": "d39d977837414790d42ecd351f59da887d7c41f1a62b5463475bf1c6dc1bd556",
        "key": "WnjdH1xTxVBpHMezzIRhPEbbxmxtIYvr"
    }))