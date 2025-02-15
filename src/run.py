import app.setup as setup

app = setup.create_app()

if __name__ == '__main__':
    app.run(debug=True, port=app.config['port'])