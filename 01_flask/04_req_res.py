from flask import Flask ,render_template,request
from flask import Response, make_response
app = Flask(__name__) 

@app.route('/area')  
def area():
    pi = request.args.get('pi','3.14') #pi 값을 주지않으면 3.14을 디폴트로 하겠다는 뜻
    radius = request.args['radius']
    s = float(pi)*float(radius)*float(radius)
    return f'pi={pi}, radius={radius},area={s}'      #http://localhost:5000/area?pi=3.14159&radius=5

@app.route('/login', methods=['GET','POST']) 
def login() :
    if request.method == 'GET':
        return render_template('03_login.html')  
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        # pwd = request.values['pwd'] values도 가능
        return f'uid={uid}, pwd={pwd}'

@app.route('/response')  
def response_fn():
    custom_res = Response('Custom Response',200,{'test':'ttt'})
    return make_response(custom_res)

if __name__ == '__main__':
    app.run(debug=True)

#get 은 args  post는 form