from flask import Blueprint, render_template, request, session, g, redirect, url_for
from flask import current_app

from datetime import datetime, timedelta
from sklearn.datasets import load_digits
import os, joblib,json,requests

from my_util.weather import get_weather

from urllib.parse import quote

nl_bp = Blueprint('nl_bp', __name__)

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

@nl_bp.route('/trVo', methods=['GET', 'POST'])
def trVo():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,'st':0,
            'cf':0, 'ac':0, 're':0, 'cu':0,'nl':1}
    if request.method == 'GET':
        languages =  { '영어' : 'en', '일본어':'jp', '중국어':'cn', '프랑스어':'fr','스페인어': 'es'}
        return render_template('nat_lang/trVo.html', menu=menu, weather=get_weather(),languages=languages)
    else:
        text = request.form['text'] 
        
        if request.form['optradio'] == 'translation':
            #텍스트번역일 경우-네이버
            lang = request.form['lang']
            with open('static/data/papago_key.json') as nkey:
                json_str = nkey.read(100)
            json_obj =json.loads(json_str)
            client_id =list(json_obj.keys())[0]
            client_secret=json_obj[client_id]

            n_url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
            
            
            n_mapping = {'en':'en', 'jp':'ja', 'cn':'zh-CN', 'fr':'fr', 'es':'es'}

            val = {
                    "source": 'ko',
                    "target": n_mapping[lang],
                    "text": text
            }   #"target": n_mapping[lang]
 
            headers = {
                "X-NCP-APIGW-API-KEY-ID": client_id,
                "X-NCP-APIGW-API-KEY": client_secret
            }
            
            result= requests.post(n_url,data=val,headers=headers).json()            
            n_text =result['message']['result']['translatedText']

            #텍스트번역일 경우-카카오
            with open('static/data/kakaoaikey.txt') as kfile:
                kai_key = kfile.read(100)
            text = text.replace('\n',''); text = text.replace('\r','')
            k_url = f'https://dapi.kakao.com/v2/translation/translate?query={quote(text)}&src_lang=kr&target_lang={lang}'
            result = requests.get(k_url,
                              headers={"Authorization": "KakaoAK "+kai_key}).json()
            tr_text_list = result['translated_text'][0]  #[0]은 하나만 
            k_translated_text = '\n'.join([tmp_text for tmp_text in tr_text_list])
            k_text= k_translated_text
            
            return render_template('nat_lang/translation_res.html', menu=menu,text=text,n_text=n_text,k_text=k_text,lang=lang,
                                 weather=get_weather())
        else:
            #음성일 경우
            speaker = request.form['speaker']
            pitch = request.form['pitch']
            volume = request.form['volume']
            speed = request.form['speed']
            emotion = request.form['emotion']
            

            with open('static/data/clova_key.json') as nkey:
                json_str = nkey.read(100)
            json_obj =json.loads(json_str)
            client_id =list(json_obj.keys())[0]
            client_secret=json_obj[client_id]

            v_url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

            headers = {
                "X-NCP-APIGW-API-KEY-ID": client_id,
                "X-NCP-APIGW-API-KEY": client_secret,
                "Content-Type": "application/x-www-form-urlencoded" 
            }
            # 오디오로 변환
            
            v_val = {
                "speaker": speaker,
                "speed": speed,
                "text": text,"pitch": pitch, "volume": volume, "emotion": emotion
            }
            response= requests.post(v_url,data=v_val,headers=headers)
            rescode= response.status_code

            audio_file = os.path.join(current_app.root_path,'static/img/cpv.mp3')

            if(rescode == 200):            
                with open(audio_file, 'wb') as f:
                    f.write(response.content)
            mtime = int(os.stat(audio_file).st_mtime)
           
            
            
            return render_template('nat_lang/voice_res.html', menu=menu, text=text,v_val=v_val, 
                                mtime=mtime, weather=get_weather())



       

       
