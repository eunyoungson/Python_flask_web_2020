from flask import Blueprint, render_template, request, session, g
from flask import current_app, redirect, url_for
from datetime import datetime, timedelta
import os, folium, json
import pandas as pd
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from my_util.weather import get_weather
import db.db_module as dm
import my_util.covid_util as cu

covid_bp = Blueprint('covid_bp', __name__)

def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@covid_bp.route('/region')
def region():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_region_daily(date)

    return render_template('covid/region.html', menu=menu, weather=get_weather_main(),
                            date=date, rows=rows)

@covid_bp.route('/update_region/<date>')
def update_region(date):
    rows = dm.get_region_daily(date)
    if len(rows) == 0:
        cu.get_region_by_date(date)

    return redirect(url_for('covid_bp.region')+f'?date={date}')

@covid_bp.route('/agender')
def agender():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_agender_daily(date)

    return render_template('covid/agender.html', menu=menu, weather=get_weather_main(),
                            date=date, rows=rows)

@covid_bp.route('/update_agender/<date>')
def update_agender(date):
    rows = dm.get_agender_daily(date)
    if len(rows) == 0:
        cu.get_agender_by_date(date)

    return redirect(url_for('covid_bp.agender')+f'?date={date}')

@covid_bp.route('/region_seq', methods=['GET', 'POST'])
def region_seq():
    if request.method == 'GET':
        mpl.rc('font', family='Malgun Gothic')
        mpl.rc('axes', unicode_minus=False)
        menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
        rows = dm.get_region_items_by_gubun('stdDay, incDec', '합계')
        cdf = pd.DataFrame(rows, columns=['기준일','전국'])
        metro_list = ['서울', '부산', '대구', '인천', '대전', '광주', '울산', '세종', 
                    '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '제주']
        for metro in metro_list:
            results = dm.get_region_items_by_gubun('stdDay, incDec', metro)
            df = pd.DataFrame(results, columns=['기준일', metro])
            cdf = pd.merge(cdf, df, on='기준일')
        cdf['기준일'] = pd.to_datetime(cdf['기준일'])
        cdf.set_index('기준일', inplace=True)

        region_str = request.args.get('region', '전국 서울 경기 대구')
        region_list = region_str.split()
        img_file = os.path.join(current_app.root_path, 'static/img/covid_seq.png')
        plt.figure()
        for region in region_list:
            cdf[region].plot(grid=True, figsize=(12,8))
        plt.title('지역별 확진자 추이', fontsize=15)
        plt.legend()
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)
        region_str = ', '.join(region for region in region_list)
        metro_list = ['전국', '서울', '부산', '대구', '인천', '대전', '광주', '울산', '세종', 
                    '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '제주']

        return render_template('covid/region_seq.html', menu=menu, weather=get_weather_main(),
                                mtime=mtime, metro_list=metro_list, region_str=region_str)

    else:
        region_list = request.form.getlist('metro')
        #print(region_list)
        region_str = ' '.join(region for region in region_list)
        return redirect(url_for('covid_bp.region_seq')+f'?region={region_str}')

@covid_bp.route('/age_seq', methods=['GET', 'POST'])
def age_seq():
    if request.method == 'GET':
        mpl.rc('font', family='Malgun Gothic')
        mpl.rc('axes', unicode_minus=False)
        menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
        rows = dm.get_agender_items_by_gubun('stdDay, confCase', '0-9')
        adf = pd.DataFrame(rows, columns=['기준일','0-9'])
        adf = cu.get_daily(adf, '0-9', '0-9세')
        age_dict = {'10-19':'10-19세', '20-29':'20-29세', '30-39':'30-39세', '40-49':'40-49세',
                    '50-59':'50-59세', '60-69':'60-69세', '70-79':'70-79세', '80 이상':'80세이상'}
        for key, value in age_dict.items():
            rows = dm.get_agender_items_by_gubun('stdDay, confCase', key)
            tdf = pd.DataFrame(rows, columns=['기준일', key])
            tdf = cu.get_daily(tdf, key, value)
            adf = pd.merge(adf, tdf, on='기준일')
        adf['기준일'] = pd.to_datetime(adf['기준일'])
        adf.set_index('기준일', inplace=True)

        age_str = request.args.get('age', '20-29세 50-59세 60-69세')
        age_list = age_str.split()
        img_file = os.path.join(current_app.root_path, 'static/img/covid_age_seq.png')
        plt.figure(figsize=(12,8))
        for age in age_list:
            adf[age].plot(grid=True)
        plt.title('연령별 확진자 추이', fontsize=15)
        plt.legend()
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)
        age_str = ', '.join(age for age in age_list)
        age_list = ['0-9세', '10-19세', '20-29세', '30-39세', '40-49세',
                    '50-59세', '60-69세', '70-79세', '80세이상']

        return render_template('covid/age_seq.html', menu=menu, weather=get_weather_main(),
                                mtime=mtime, age_list=age_list, age_str=age_str)

    else:
        age_list = request.form.getlist('age')
        #print(age_list)
        age_str = ' '.join(age for age in age_list)
        return redirect(url_for('covid_bp.age_seq')+f'?age={age_str}')