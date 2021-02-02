from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.datasets import load_digits
import os, joblib
import pandas as pd
import matplotlib.pyplot as plt
from my_util.weather import get_weather
import re
from sklearn.pipeline import Pipeline
from konlpy.tag import Okt

aclsf_bp = Blueprint('aclsf_bp', __name__)

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

@aclsf_bp.before_app_first_request
def before_app_first_request():
    global imdb_count_lr, imdb_tfidf_lr
    #global news_count_lr, news_tfidf_lr, news_tfidf_sv
    print('============ Advanced Blueprint before_app_first_request() ==========')
    imdb_count_lr = joblib.load('static/model/pipeline_cl.pkl')
    imdb_tfidf_lr = joblib.load('static/model/pipeline_tl.pkl')
    #news_count_lr = joblib.load('static/model/news_count_lr.pkl')
    #news_tfidf_lr = joblib.load('static/model/news_tfidf_lr.pkl')
    #news_tfidf_sv = joblib.load('static/model/news_tfidf_sv.pkl')

@aclsf_bp.route('/digits', methods=['GET', 'POST'])
def digits():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,'st':0,
            'cf':0, 'ac':1, 're':0, 'cu':0,'nl':0}
    if request.method == 'GET':
        return render_template('advanced/digits.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        index_list = list(range(index, index+5))
        digits = load_digits()
        df = pd.read_csv('static/data/digits_test.csv')
        img_index_list = df['index'].values
        target_index_list = df['target'].values
        index_list = img_index_list[index:index+5]

        scaler = joblib.load('static/model/digits_scaler.pkl')
        test_data = df.iloc[index:index+5, 1:-1]
        test_scaled = scaler.transform(test_data)
        label_list = target_index_list[index:index+5]
        lrc = joblib.load('static/model/digits_lr.pkl')
        svc = joblib.load('static/model/digits_sv.pkl')
        rfc = joblib.load('static/model/digits_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/digit')
        for k, i in enumerate(index_list):
            plt.figure(figsize=(2,2))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(k+1) + '.png'
            plt.imshow(digits.images[i], cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index_list, 'label':label_list,
                       'pred_lr':pred_lr, 'pred_sv':pred_sv, 'pred_rf':pred_rf}
        
        return render_template('advanced/digits_res.html', menu=menu, mtime=mtime,
                                result=result_dict, weather=get_weather())

@aclsf_bp.route('/imdb', methods=['GET', 'POST'])
def news():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,'st':0,
            'cf':0, 'ac':1, 're':0, 'cu':0,'nl':0}
    
    if request.method == 'GET':
        return render_template('advanced/imdb.html',menu=menu, weather=get_weather())
    else: 
        label = '직접 확인'
        test_data = []
        if request.form['optradio'] == 'index':

            index = int(request.form['index'] or 0)
            df = pd.read_csv('F:/workspace/Flask/03_Module/static/data/imdb_test1.csv')
            test_data.append(df.iloc[index,0])  #test_data.append(df_test.iloc[index, 0])
            label = '긍정' if df.sentiment[index] else '부정'
        else:
            
            test_data.append(request.form['review'])


        #news_pcl = joblib.load('static/model/pipeline_cl.pkl')
        #news_ptl = joblib.load('static/model/pipeline_tl.pkl')
        #pred_cl = imdb_count_lr.predict(test_data)
        #pred_tl = imdb_tfidf_lr.predict(test_data)
        pred_cl = '긍정' if imdb_count_lr.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if imdb_tfidf_lr.predict(test_data)[0] else '부정'
        
        result_dict = {'label':label, 
                       'pred_cl':pred_cl,
                       'pred_tl': pred_tl}
        
        return render_template('advanced/imdb_res.html', menu=menu, review=test_data[0], 
                                res=result_dict, weather=get_weather())

@aclsf_bp.route('/naver', methods=['GET', 'POST'])
def naver():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,'st':0,
            'cf':0, 'ac':1, 're':0, 'cu':0,'nl':0}
    
    if request.method == 'GET':
        return render_template('advanced/naverR.html',menu=menu, weather=get_weather())
    else: 
        
       
        if request.form['optradio'] == 'index':
            #int로 들어올때
            index = int(request.form['index'] or 0)
            df = pd.read_csv('F:/workspace/machine-Learning/00.data/naverMovie/test.tsv' ,sep='\t')
            #test_data.append(df.iloc[index,2])  
            org_review = df.document[index]
            state = '긍정' if df.label[index] else '부정'
        else:
            #직접입력
            org_review = request.form['review']
            state = '직접 입력'
            

        
        test_data = []
        
        review= re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","",org_review)
        okt = Okt()
        morphs =okt.morphs(review,stem= True)
        stopwords = [ '의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
        temp_X = ' '.join([word for word in morphs if not word in stopwords])
        test_data.append(temp_X)


        naver_count_lr = joblib.load('static/model/Npipeline_cl.pkl')
        naver_tfidf_lr = joblib.load('static/model/Npipeline_tl.pkl')
        naver_count_nv = joblib.load('static/model/Npipeline_cn.pkl')
        naver_tfidf_nv = joblib.load('static/model/Npipeline_tn.pkl')

        
        pred_cl = '긍정' if naver_count_lr.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if naver_tfidf_lr.predict(test_data)[0] else '부정'
        pred_cn = '긍정' if naver_count_nv.predict(test_data)[0] else '부정'
        pred_tn = '긍정' if naver_tfidf_nv.predict(test_data)[0] else '부정'
        
        result_dict = {'state':state, 
                       'pred_cl':pred_cl, 'pred_cn':pred_cn, 'pred_tn': pred_tn,
                       'pred_tl': pred_tl}
        
        return render_template('advanced/naverR_res.html', menu=menu, review=org_review, 
                                res=result_dict, weather=get_weather())
