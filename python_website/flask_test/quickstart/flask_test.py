from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/projects/')
def projects():
    """
    这个可以输入  ../projects  会自动转到 /projects/
    无法在创建 一个
@app.route('/projects')
def projects():
    return 'this is in /projects'
    这个会报错
    而下面的 about 则必须输入 ../about 而不是 ../about/ --> 会报错 not found
    :return: 
    """
    return 'this is in /project/'


@app.route('/user/<username>')
def input_username(username):
    return username


@app.route('/about')
def about():
    return 'this is in about'


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='127.0.0.1', port=4166)

columns = 1
