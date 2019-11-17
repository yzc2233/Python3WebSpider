#导入Flask类
from flask import Flask,url_for
#创建该类的实例，第一个参数是应用模块的参数或者包的名字，
# 如果使用单一的模块（如本实例），则应该使用“__name__”参数
#如果作为模块导入，则应该设置参数为实际的导入名。这样Flask才知道去哪里找模板、静态文件等
app = Flask(__name__)

#使用route()装饰器告诉Flask是，什么样的URL能触发函数
@app.route('/')
#定义函数，这个函数要显示在用户浏览器中的信息
def hello_world():
    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    #显示该用户的用户信息
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    #根据ID显示文章，ID是整形数据
    return 'Post %s' % post_id

@app.route('/url/')
def get_url():
    #根据ID显示文章，ID是整形数据
    return url_for('show_post',post_id=2)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()



if __name__ == '__main__':
    #run()函数让应用运行在本地服务器上
    #debug=True启用调试模式，服务器会在代码修改后自动重新载入
    app.run(debug=True)


















