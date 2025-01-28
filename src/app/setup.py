from flask import Flask, make_response
from . import routes
import app.models.config as config

app1=Flask(__name__)
app1.register_blueprint(routes.built_blueprint)

@app1.after_request
def after(resp):
    '''
    被after_request钩子函数装饰过的视图函数 
    ，会在请求得到响应后返回给用户前调用，也就是说，这个时候，
    请求已经被app.route装饰的函数响应过了，已经形成了response，这个时
    候我们可以对response进行一些列操作，我们在这个钩子函数中添加headers，所有的url跨域请求都会允许！！！
    '''
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = config.panelconfig.data["site-url"]
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

def run(debug):
    app1.run(debug=debug)
