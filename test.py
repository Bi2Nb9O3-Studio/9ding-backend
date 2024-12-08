from flask import Flask

app = Flask(__name__)


class MyView:

    @app.route('/')
    def index(self):
        return 'Hello, World!'


view = MyView()

if __name__ == '__main__':
    app.run()
