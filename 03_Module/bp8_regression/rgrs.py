from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from my_util.weather import get_weather
import seaborn as sns
import matplotlib.pyplot as plt 


rgrs_bp = Blueprint('rgrs_bp', __name__)

def get_weather_main():
    ''' weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60) '''
    weather = get_weather()
    return weather

@rgrs_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0, 'st':0,
            'cf':0, 'ac':0, 're':1, 'cu':0,'nl':0}
    if request.method == 'GET':
        return render_template('regression/iris.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        feature_name = request.form['feature']
        column_dict = {'sl':'Sepal length', 'sw':'Sepal width', 
                       'pl':'Petal length', 'pw':'Petal width', 
                       'species':['Setosa', 'Versicolor', 'Virginica']}
        column_list = list(column_dict.keys())

        df = pd.read_csv('static/data/iris_train.csv')
        df.columns = column_list
        X = df.drop(columns=feature_name, axis=1).values
        y = df[feature_name].values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/iris_test.csv')
        df_test.columns = column_list
        X_test = df_test.drop(columns=feature_name, axis=1).values[index]
        pred_value = np.dot(X_test, weight.T) + bias

        x_test = list(df_test.iloc[index,:-1].values)
        x_test.append(column_dict['species'][int(df_test.iloc[index,-1])])
        org = dict(zip(column_list, x_test))
        pred = dict(zip(column_list[:-1], [0,0,0,0]))
        pred[feature_name] = np.round(pred_value, 2)
        return render_template('regression/iris_res.html', menu=menu, weather=get_weather(),
                                index=index, org=org, pred=pred, feature=column_dict[feature_name])

@rgrs_bp.route('/boston', methods=['GET', 'POST'])
def boston():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0, 'st':0,
            'cf':0, 'ac':0, 're':1, 'cu':0,'nl':0}
    if request.method == 'GET':
        descriptions = ['범죄율','2.5만평 초과거주비율','비상업지역비율','찰스강 근처여부','농축일산화질소',
                        '방의 갯수','노후주택비율','주요시설접근지수','방사형도로접근지수','재산세 세율','학생/교사비율',
                        '흑인비율','하위계층비율','본인소유주택가격']
        
        feature_name = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
                        'TAX', 'PTRATIO', 'B', 'LSTAT','MEDV']
        return render_template('regression/boston.html', menu=menu, weather=get_weather(),feature_name=feature_name,descriptions=descriptions )
    else:
        index = int(request.form['index'])
        feature_name = request.form.getlist('feature')
        df = pd.read_csv('static/data/boston_train1.csv')
        column_list =df.columns 
        X = df[feature_name].values
        y = df.price.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/boston_test1.csv')
        
        X_test = df_test[feature_name].values[index,:]
        y_test = df_test.price.values[index]
        pred = np.dot(X_test, weight.T) + bias #tmp=lr.predict(X_test.reshape(1,-1))
        pred =np.round(pred,2)  #pred=np.round(tmp[0])

        result = {'index': index, 'feature':feature_name,'y':y_test,'pred':pred }
        org = dict(zip(df.columns[:-1], df_test.iloc[index,:-1]))
       

        #그래프
       
        fig, asx = plt.subplots(figsize=(16,8), ncols=4, nrows=2)
        
        for i, feature in enumerate(feature_name):
            row, col = int(i/4), i%4
            sns.regplot(x=feature, y='price', data=df, ax=asx[row][col])
        img_file = os.path.join(current_app.root_path, 'static/img/boston.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)
        # column_list = list(boston.feature_names)=list(df.columns)
        return render_template('regression/boston_res.html', menu=menu, weather=get_weather(),
                                res= result, org=org, mtime=mtime)


