import os
import subprocess
import sys,shutil
if "--post-up-date" in sys.argv:
    argvs = sys.argv[1:]
    argvs.remove("--post-up-date")
    subprocess.Popen([sys.executable, __file__, "--clean-update"]+argvs,shell=True)
    print("Post update finished")
    sys.exit()
if "--clean-update" in sys.argv:
    shutil.rmtree("./tmp1",ignore_errors=True)
    print("Cleaned up.Update Finished")
import app.models.database as db
os.makedirs("./configs/", exist_ok=True)
os.makedirs("./logs/", exist_ok=True)
os.makedirs("./models/", exist_ok=True)
os.makedirs("./bundle/", exist_ok=True)
import sys
import app.setup
import app.auth
if __name__ == "__main__":
    debug="--debug" in sys.argv
    app.setup.run(debug=debug)