if __name__ == "__main__":
    import os
    os.makedirs("./configs/", exist_ok=True)
    os.makedirs("./logs/", exist_ok=True)
    os.makedirs("./models/", exist_ok=True)
    os.makedirs("./bundle/", exist_ok=True)
    import auto_update as atp
    import app.models.database as db
    import app.setup
    import app.auth

    atp.download_font()
    atp.update_bundle()
    app.setup.app.run()