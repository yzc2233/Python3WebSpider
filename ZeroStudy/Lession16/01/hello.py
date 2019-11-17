#导入Flask类
from flask import Flask
#创建该类的实例，第一个参数是应用模块的参数或者包的名字，
# 如果使用单一的模块（如本实例），则应该使用“__name__”参数
#如果作为模块导入，则应该设置参数为实际的导入名。这样Flask才知道去哪里找模板、静态文件等
app = Flask(__name__)

#使用route()装饰器告诉Flask是，什么样的URL能触发函数
@app.route('/')
#定义函数，这个函数要显示在用户浏览器中的信息
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    #run()函数让应用运行在本地服务器上
    #debug=True启用调试模式，服务器会在代码修改后自动重新载入
    app.run(debug=True)


















