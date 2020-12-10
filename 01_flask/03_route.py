from flask import Flask ,render_template,request
app = Flask(__name__) 

@app.route('/')  
def index():
    return 'hello Flask!'

@app.route('/user/<uid>')    #String Type
def string_fn(uid) :
    return uid

@app.route('/int/<int:number>') #int type
def int_fn(number) :
    return str(100*number)

@app.route('/float/<float:number>') #float type   웹에 http://localhost:5000/float/3.1456
def float_fn(number) :
    return str(10*number)

@app.route('/path/<path:path>') #path type  http://localhost:5000/path/test/kkk
def path_fn(path) :
    return f'path {path}'

@app.route('/login', methods=['GET','POST']) 
def login() :
    if request.method == 'GET':
        return render_template('03_login.html')  #show the login form
    else:
        return render_template('02_welcome.html')  #do the login  process

if __name__ == '__main__':
    app.run(debug=True)