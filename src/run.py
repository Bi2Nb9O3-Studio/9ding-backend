import threading
import app.setup as setup
import auto_update as au

app = setup.create_app()

if __name__ == '__main__':
    au.start_thread()
    app.run(debug=True, port=app.config['port'])