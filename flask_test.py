# 极简Flask测试
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>如果您看到这个，Flask工作正常</h1>"

if __name__ == '__main__':
    print("Flask服务器启动在: http://127.0.0.1:5000")
    app.run(debug=True) 