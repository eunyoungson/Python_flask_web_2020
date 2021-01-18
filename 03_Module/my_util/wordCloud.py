import numpy as np 
import pandas as pd 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import nltk, re
from konlpy.tag import Okt

def engCloud(text, stop_words, mask_file, img_file, max_words=1000):
    stopwords = set(STOPWORDS)
    for sw in stop_words:
        stopwords.add(sw)

    if mask_file == None:
        wc = WordCloud(background_color='black', width=800, height=800, max_words=max_words, stopwords=stopwords)
    else:
        mask = np.array(Image.open(mask_file))
        wc = WordCloud(background_color='white', width=800, height=800, max_words=max_words, mask=mask, stopwords=stopwords)
    wc = wc.generate(text)
    plt.figure(figsize=(8,8), dpi=100)
    ax = plt.axes([0,0,1,1])
    #plt.imshow(wc, interpolation='bilinear')
    plt.imshow(wc, interpolation='nearest', aspect='equal')
    plt.axis('off')
    plt.savefig(img_file)

def hanCloud(text, stop_words, mask_file, img_file, max_words=1000):
    mpl.rc('font', family='Malgun Gothic')
    mpl.rc('axes', unicode_minus=False)
    okt = Okt()
    tokens = okt.nouns(text)
    new_text = []
    for token in tokens:
        text = re.sub('[a-zA-Z0-9]', '', token)
        new_text.append(text)
    stop_words = ['선물','추천','것','가격','여친','제품','여자친구','제','요','더','고급', '크리스마스','것','커플','저','수','요','남자','거','사랑','제','더','사람','분','제품','직접','비','고민','가성','전','가능','를','한번','연인','친구','님','포장','용','등','준','하나','그냥','와우','자존심','건','걸','수도','저희','리얼리티','호캉스','여름방학','정유미','최우식','박서준','여러','연예인','통해','최신','유행','아이템','소개','후','국내','똑','상용', '맘',  '마스크', '스트랩', '종류','종류', '별로', '개성', '컨셉', '달라', '얼룩', '오피스', '데','사용','때','수','곳','고흐', '모네', '르누아르', '작품', '건물', '유리창', '햇살', '기분',
    '판매','때','참고','하나','해','한번','제작','용','준','디자인','거','네이버','사람','일리', '포멀룩', '연령', '안성맞춤', '망토', '담요', '웰컴', '키트','생신', '동생', '동영상','아버지', '아버지', '인도', '한국', '맛', '또', '케익', '조각', '보고', '충격',
    '배송','중','정말','후기','감동','위생', '앞', '준비', '예정', '클릭', '홈', '최고', '메이드','자바라', '거치', '침대', '핸드폰', '거치', '스마트폰', '아이폰', '어디', '매치', '에센', '동생', '집','다른', '다른', '녹색','좀','엄', '청','강화',
    '커플','가능','저','사랑','생각','사용','개','세대','인기','상품','직접','브랜드','학', '다리', '코브라', '남친','얼마','지인', '집들이', '무척', '파파', '병아리', '무드등','구색', '운동', '홈트', '고진','스텝', '퍼', '투맨', '무난','그때', '공원', '케밥', '케밥', '만큼', '사이즈', '사이즈', '여기','만큼', '사이즈', '사이즈', '여기','인분', '간', '마트', '채소', '이', '마트','개월','고퀄','짐','하하','너','금방','관심','마너','살짝',
    '남편','날','킨더','소스','소스', '듬뿍','맛남','소스','벌이','자꾸','만','마지막','간','아빠', '모근','엄마','리스트','곳','때','우리','또','좀','주로','사실','보고','평소','여름입','어디','이번','번','이유','훌쩍','저기','품목','나름','개념','산다','얼마나','처럼','티나','기대','보기','치면','바삭','요리','애정','박','순위','불구','대부분','시기','군데','모두','상태','걱정','요것','역삼역','편이','기도','태그','부탁','흡수','단계'
    '선택','곳','모양','마감','요즘','오늘','가지','남녀','그냥','위','페이', '막상', '은', '와중', '독일어','냄새','프리','제일','저렴','요건','로','크기','보통','어디','옆','단점','알','계속','소품','두','예약','구','사이트','마무리','일',
    '마음','부담','남자','협찬','전','핸드','의미','변경','도움','색상','아래','포장', '강력', '바로', '주문', '채택', '이용', '포함', '작성자', '수수료', '근교', '나가야', '합리', '아예','나중', '우왕좌왕', '특권', '정해진', '특별', '일반', '전시', '고갱',
    '처','조금','꾹', '해쥬세', '이글', '에드픽', '지급', '바디', '필', '로우','구이', '부부', '요새', '살','타르트', '달달', '공부', '정이','문화', '다시', '만날', '그땐', '기억', '인스타', '소식', '테', '무료', '미술관', '키스', '링전','옆', '처음', '만난', '당시', '얼마나', '기회','뭐해', '방식', '애정', '팅', '스스로', '하하', '요것','상태', '지난' , '각종', '저기', '마너', '위해',
    '요것', '역삼역', '다만', '훌쩍', '리', '페이지', '전부', '담', '대부분', '실화', '두께', '하하', '비교', '최근', '직구', '오른쪽', '기대', '군데',
    '하루','정도','처리','보시','심플','가장','여성','때문','정보','볼', '자','코', '작별인사', '내', '언니네', '밥','그림','사실','역시','손','주로','보고','로','남편','청소','주','둘','이번','약간','완전','이제','아예','기본','느낌','한국',
    '독서','주소','쇼핑','링크','이니셜','기념일','실용', '바나', '나리', '빙','독일', '제일', '정신', '주', '시험', '베를린', '여행', '후', '일주일', '후','원래', '우리', '하우스', '우리','간다', '기약', '아마', '약간','수료증', '커피타임', '카페', '딸기','하하','군데','목록',
    '헤어','질문','친구','스토어','아주','할인','쫀득', '마약', '마이크로', '에어','가족', '인사', '한참', '여름', '도', '도', '날씨', '계속', '벌써', '가을','가을', '분위기', '우선', '겔젠키르헨', '할머니', '할아버지', '우린', '항상', '가면', '아침','운영','뭐해','스스로','팔고','두께','티나','산다','안녕','위해','개월','일요일','목적','오른쪽','대도',
    '스','이면','남','지금','센스', '내셔널', '지오', '그래픽', '스몰','공용','현재','쿠팡','행사','중이','뭘','뭐','물질','소정','폴','나나','남자친구','답변','속','그','음','글','구매','말','줄','일단','주인공','겨울','사이','생일','더욱','방법','자신','이건','정리','등등','나','답변','매장', '관리', '고생', '살라미', '과일', '주기','연어','강화','한텐','진짜','아이','물','사실','안','이번','거의','유럽','물건','역시','사이트','성분','유치원','알','느낌','다음','번','먼저','피부','졸업','비견','이제','재미','주로','로','나라','엄마','발레','완전','디아','양제','꽃집','사','손','아들','꽃','리스트','이유','홍콩','종합','매우','예약','점','검색','이유','미국','차이','의','편','프리','재질','암미','박스','잇몸','이름','산','택배','보통','해외','게','크기','꼭','청소','그리기','일','꽃','평소','몸','코로나','얼굴','잔열','자체','파티','단점','음식','입','봄','단연','늘','콕','먹기','요건','설명','누타','꽃다발','프랑스','두','뭔가','보','쓰기','시작','난','못','실제','중세','뜻','메달','유로','여','마개','보관','대략','소품','나무','돌','왜','일산','마무리','댓글','매일','일상','시간','둘','부분','끝','형','자기','냄새','쓰기','메달','진열','꽤','우리나라','위주','얼씬','기본','구','뿐','훠','내일','대형','유','무','포스트','발견','픽업']
    
    new_text = [word for word in new_text if word not in stop_words]
    han_text = nltk.Text(new_text, name='한글 텍스트')
    data = han_text.vocab().most_common(300)
    if mask_file == None:
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf',
                        width=800, height=800,
                        relative_scaling = 0.2, background_color='black',
                        ).generate_from_frequencies(dict(data))
    else:
        mask = np.array(Image.open(mask_file))
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf',
                        width=800, height=800,
                        relative_scaling = 0.2, mask=mask,
                        background_color='white',
                        ).generate_from_frequencies(dict(data))

    plt.figure(figsize=(8,8), dpi=100)
    ax = plt.axes([0,0,1,1])
    #plt.imshow(wc, interpolation='bilinear')
    plt.imshow(wc, interpolation='nearest', aspect='equal')
    plt.axis('off')
    plt.savefig(img_file)

    