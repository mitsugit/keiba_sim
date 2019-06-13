from django.shortcuts import render
from django.http import HttpResponse
# from django.views.generic import TemplateView
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.db.models import Q
# from .oricalc import simplecalc

from .martingale_m import martingale



from .forms import LogicTestForm,RaceStteiForm, LogicForm,RaceRecordForm,RaceRecordForm,RecordButtonForm 

from .models import  RaceData,TargetRaceData,TargetRaceID,RaceSettei #,NewLogic

from django_pandas.io import read_frame
import pandas as pd
import numpy as np

from datetime import datetime as dt

from django.core.paginator import Paginator

import copy

def __new_str__(self):
    result = ''
    for item in self:
        result += '<tr>'
        for k in item:
            result += '<td>'+str(k)+ '=' + str(item[k])+'</td>'
        result += '</tr>'
    return result

QuerySet.__str__ = __new_str__

def home(request):
    
    x = simplecalc(12)
    
    params = {
        'title':'ホーム画面です',
        'x':x
        }
    return render(request, 'keiba/home.html', params)


def index(request):
    
    params = {
        'title':'モード選択画面'
        }
    return render(request, 'keiba/index.html', params)

def logic(request):
    if(request.method == 'POST'):
        form = LogicForm(request.POST)

        request.session['form_data'] = request.POST
        QueryDict = request.session['form_data'] 
        print(QueryDict)


        target_race = QueryDict.__getitem__('target_race')
        print(target_race)
        
        budget = QueryDict.__getitem__('budget')
        initial_bet = QueryDict.__getitem__('initial_bet')
        select_or_manual = QueryDict.__getitem__('select_or_manual')
        
        # disableでセッションの辞書にキーが入っていない場合にエラーにならないように場合分け
        if 'bet_way' in QueryDict.keys():
            bet_way = QueryDict.__getitem__('bet_way')
        else:
            bet_way = ""

        fix_or_variable = QueryDict.__getitem__('fix_or_variable')
        if 'fix_bet' in QueryDict.keys():
            fix_bet = QueryDict.__getitem__('fix_bet')
        else:
            fix_bet =""
        if 'reset_when_hit' in QueryDict.keys():
            reset_when_hit = QueryDict.__getitem__('reset_when_hit')
        
        lost_bet_reset = QueryDict.__getitem__('lost_bet_reset')
        win_bet_reset = QueryDict.__getitem__('win_bet_reset')
        stopbet_bylost = QueryDict.__getitem__('stopbet_bylost')
        stopbet_bymaxbet = QueryDict.__getitem__('stopbet_bymaxbet')

        if 'stop_when_hit' in QueryDict.keys():
            stop_when_hit = QueryDict.__getitem__('stop_when_hit')
        target_jockey = QueryDict.__getitem__('target_jockey')
        odds_minimum = QueryDict.__getitem__('odds_minimum')
        odds_max = QueryDict.__getitem__('odds_max')


        countdown_ninki = QueryDict.__getitem__('countdown_ninki')
        countdown_jockey = QueryDict.__getitem__('countdown_jockey')

        start_bet_ninki = QueryDict.__getitem__('start_bet_ninki')
        start_bet_jockey = QueryDict.__getitem__('start_bet_jockey')
        target_place = QueryDict.__getitem__('target_place')


        #登録する
        obj = Logic()
        friend = LogicRecordForm(request.POST, instance=obj)
        friend.save()



        print(type(countdown_ninki))

        if countdown_ninki != "":
            countdown_ms1 = countdown_ninki+"番人気が"+start_bet_ninki+"回以上"+target_place+"着外でベット開始"
        if countdown_jockey != "":
            countdown_ms2 = countdown_jockey+"が"+start_bet_ninki+"回以上"+target_place+"着外でベット開始"

        print(countdown_ms2)

    else:
        form = LogicForm
        countdown_ms1 =""
        countdown_ms2 =""

    params = {
        'form':form,
        'countdown_ms1':countdown_ms1,
        'countdown_ms2':countdown_ms2,
    }


    return render(request, 'keiba/logic.html', params)


def result(request):
    if(request.method == 'POST'):


        request.session['form_data'] = request.POST
        QueryDict = request.session['form_data'] 
        print(QueryDict)



        # 全オブジェクトデータを取得
        racedata = RaceData.objects.all()   
       
        # データをデータフレーム化
        df = read_frame(racedata)

       
        target_race = QueryDict.__getitem__('target_race')
        print(target_race)
        obj = TargetRaceID.objects.get(id=target_race)
        raceID = obj.target_RaceID
        raceID_list = [x.strip() for x in raceID.split(',')]
        print("ターゲットレースID",raceID_list)
        target_df = df[df["race_ID"].isin(raceID_list)]
        print(target_df)

        

        new_df = target_df[(target_df['place_number']==1)].loc[:, ["race_place","race_number","win_ninki","from_odds","win_return"]]
        

        #新たなデータフレーム から.valuesでarrayに変換し、そのarrayをリストに変換する
        target_list_ninki = new_df["win_ninki"].values.tolist()
        target_list_return = new_df["win_return"].values.tolist()


        


        




        budget = QueryDict.__getitem__('budget')
        print(type(budget))
        budget = int(budget)
        print(type(budget))
        # budget = simplecalc(budget)
        # print(budget)
        initial_bet = QueryDict.__getitem__('initial_bet')
        
        initial_bet = int(initial_bet)
        
        stopbet_bymaxbet = QueryDict.__getitem__('stopbet_bymaxbet')
        if stopbet_bymaxbet != "":
            stopbet_bymaxbet = int(stopbet_bymaxbet)
        else:
            stopbet_bymaxbet = 10000000000000000 

        
        
        select_or_manual = QueryDict.__getitem__('select_or_manual')
        
        # disableでセッションの辞書にキーが入っていない場合にエラーにならないように場合分け
        if 'bet_way' in QueryDict.keys():
            bet_way = QueryDict.__getitem__('bet_way')
        else:
            bet_way = ""

        fix_or_variable = QueryDict.__getitem__('fix_or_variable')
        if 'fix_bet' in QueryDict.keys():
            fix_bet = QueryDict.__getitem__('fix_bet')
        else:
            fix_bet =""
        if 'reset_when_hit' in QueryDict.keys():
            reset_when_hit = QueryDict.__getitem__('reset_when_hit')
        else:
            reset_when_hit = ""

        
        lost_bet_reset = QueryDict.__getitem__('lost_bet_reset')
        win_bet_reset = QueryDict.__getitem__('win_bet_reset')
        stopbet_bylost = QueryDict.__getitem__('stopbet_bylost')

        stop_bymaxprofit = QueryDict.__getitem__('stop_bymaxprofit')
        if stop_bymaxprofit !="":
            stop_bymaxprofit = int(stop_bymaxprofit)
        else:
            stop_bymaxprofit = 10000000000000

        if 'stop_when_hit' in QueryDict.keys():
            stop_when_hit = QueryDict.__getitem__('stop_when_hit')
        target_jockey = QueryDict.__getitem__('target_jockey')
        odds_minimum = QueryDict.__getitem__('odds_minimum')
        if odds_minimum !="":
            odds_minimum = float(odds_minimum)
        else:
            odds_minimum = 1
        
        odds_max = QueryDict.__getitem__('odds_max')
        if odds_max !="":
            odds_max = float(odds_max)
        else:
            odds_max = 1000

        countdown_ninki = QueryDict.__getitem__('countdown_ninki')
        countdown_jockey = QueryDict.__getitem__('countdown_jockey')

        start_bet_ninki = QueryDict.__getitem__('start_bet_ninki')
        if start_bet_ninki !="":
            start_bet_ninki = int(start_bet_ninki)
        else:
            start_bet_ninki =""
        
        start_bet_jockey = QueryDict.__getitem__('start_bet_jockey')
        
        target_ninki = QueryDict.__getitem__('target_ninki')

        if target_ninki !='':
            target_ninki = int(target_ninki)
        else:
            target_ninki = ""
            
        target_place = QueryDict.__getitem__('target_place')

        if target_place != "":
            target_place = int(target_place)
        else:
            target_place =""


        print(type(countdown_ninki))

        if countdown_ninki != "":
            countdown_ms1 = countdown_ninki+"番人気が"+str(start_bet_ninki)+"回以上"+str(target_place)+"着外でベット開始"
        else:
            countdown_ms1 =""
        if countdown_jockey != "":
            countdown_ms2 = countdown_jockey+"が"+start_bet_ninki+"回以上"+str(target_place)+"着外でベット開始"
        else:
            countdown_ms2 =""


        new_df2 = target_df[(target_df['win_ninki']== target_ninki)].loc[:, ["from_odds"]]
        new_df2 = new_df2.reset_index(drop = True)
        # target_dataframe2 = new_df2.iloc[start_index:end_index , :]
        target_ninki_odds = new_df2["from_odds"].values.tolist()


        



        if bet_way =='マーチンゲール':
            print(martingale(budget,initial_bet,select_or_manual,fix_or_variable,fix_bet,reset_when_hit,lost_bet_reset,win_bet_reset,stopbet_bylost,target_ninki,odds_minimum,odds_max,countdown_ninki,countdown_jockey,start_bet_ninki,start_bet_jockey,target_place,target_list_ninki,target_list_return,target_ninki_odds,stopbet_bymaxbet,stop_bymaxprofit))
           
            mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,\
            count_bet,profit_result,recovery_rate\
             = martingale(budget,initial_bet,select_or_manual,fix_or_variable,\
             fix_bet,reset_when_hit,lost_bet_reset,win_bet_reset,stopbet_bylost,\
             target_ninki,odds_minimum,odds_max,countdown_ninki,countdown_jockey,\
             start_bet_ninki,start_bet_jockey,target_place,target_list_ninki,\
             target_list_return,target_ninki_odds,stopbet_bymaxbet,stop_bymaxprofit)
            
            data = [mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet,profit_result,recovery_rate]
            
            
            print(bet_list)
            # bet_list,bet_losing_streak_list,revenue_list,maxlost_list,list_empty,profit_list = martingale(budget,initial_bet,select_or_manual,fix_or_variable,fix_bet,reset_when_hit,lost_bet_reset,win_bet_reset,stopbet_bylost,target_ninki,odds_minimum,odds_max,countdown_ninki,countdown_jockey,start_bet_ninki,start_bet_jockey,target_ninki,target_place)



        print(target_list_ninki)
    

    else:
        # form = ""
        countdown_ms1 =""
        countdown_ms2 =""
        QueryDict = "",
        new_df = "",
        data = [],

    params = {
        # 'form':form,
        'countdown_ms1':countdown_ms1,
        'countdown_ms2':countdown_ms2,
        'QueryDict':QueryDict,
        'new_df':new_df,
        'data':data,

    }


    return render(request, 'keiba/result.html', params)


def racesettei(request):
    if(request.method == 'POST'):

        form = RaceStteiForm(request.POST)

        

        request.session['form_data'] = copy.deepcopy(request.POST)
        QueryDict = request.session['form_data'] 
        print(QueryDict)
        print(type(QueryDict))
        
        # print(QueryDict.__getitem__('logic_select'))
        
        form = RaceStteiForm(QueryDict)

        print(form)


        
        # print(race_place)
        
        #リスト型を代入したrace_place内の各要素を,区切りで繋げ、１つの文字列にする。
        # mojiretu = ','.join(race_place)
        # print(mojiretu)

        # 文字列をLogicSettingに保存する
        # LogicSetting.objects.create(race_place=mojiretu)
        
        #セッション情報から各変数に格納

        #セッション情報が入ったQueryDictから、race_placeをキーとして値をリスト型で取得
        place_list = QueryDict.getlist('race_place')

        race_type_list = QueryDict.getlist('race_type')
        
        start_date = QueryDict.__getitem__('start_date')
        end_date = QueryDict.__getitem__('end_date')

        from_distance = QueryDict.__getitem__('from_distance')
        to_distance = QueryDict.__getitem__('to_distance')

        win_ninki = QueryDict.__getitem__('win_ninki')
        if win_ninki != "":
            win_ninki = int(win_ninki)

        target_jockey = QueryDict.__getitem__('target_jockey')

        odds_minimum = QueryDict.__getitem__('odds_minimum')
        print(odds_minimum)
        if odds_minimum !="":
            odds_minimum = float(odds_minimum)
        else:
            odds_minimum = 1
        odds_max = QueryDict.__getitem__('odds_max')
        print(odds_max)
        if odds_max !="":
            odds_max = float(odds_max)
        else:
            odds_max = 1000

        number_horse_min = QueryDict.__getitem__('number_horse_min')
        if number_horse_min != "":
            number_horse_min= int(number_horse_min)
        else:
            number_horse_min = 1
        number_horse_max = QueryDict.__getitem__('number_horse_max')
        if number_horse_max != "":
            number_horse_max = int(number_horse_max)
        else:
            number_horse_max = 18

# レースデータの絞り込み

        # 全オブジェクトデータを取得
        racedata = RaceData.objects.all()   
       
        # データをデータフレーム化
        df = read_frame(racedata)
        
        #重複したレースIDごとに番号を付けて新しい連番を作る
        df['NewRaceID'] = pd.factorize(df['race_ID'])[0]
        #0から始まる連番を１から始める
        df['NewRaceID'] = df['NewRaceID'] +1
        print(df)


        # 開催場の絞り込み        
        place_df = df[df["race_place"].isin(place_list)]
        print("場所")
        # print(place_df)

        # 開催日の絞り込み 
        kaisai_df = df[(df["start_date"] >= start_date)&(df["end_date"] <= end_date)]
        print("期間")
        # print(kaisai_df)

        # # 距離抽出

        # In[54]:


        distance_df = df[(df.from_distance>=from_distance)&(df.from_distance<=to_distance)]
        print("期間")
        # print(distance_df)

        # # 出走馬数の指定

        # In[53]:
        print("馬数")
        print(type(number_horse_min))
        number_df = df[(df["uma_number1"]>=number_horse_min)&(df["uma_number1"]<=number_horse_max)]
        
        # print(number_df)


        # # 指定人気馬のオッズ指定
        # 
        # 

        # In[52]:


        #６番人気が１２倍以下のレースを抽出したデータフレーム を作成

        #６番人気が１０倍以上１２倍以下のレースを抽出したリスト を作成
        print("人気オッズ")
        if win_ninki != "":

            ninkiodds_list = df[(df["win_ninki"] == win_ninki)&(df["from_odds"] >=odds_minimum )&(df["from_odds"] <=odds_max)]

            #以上、以下で場合分けできるように

            #上記データフレームのままだと、６番人気の行しかない。
            #なので、上記データフレームのrace_IDをリスト化し、対象のrace_IDの全ての行が抽出されるようにする。

            #対象のrace_IDのリストを作成
            raceID_list = ninkiodds_list["race_ID"].values.tolist()

            
            ninki_odds_df = df[df["race_ID"].isin(raceID_list)]
        else:
            ninki_odds_df = df
        
        # print(ninki_odds_df)

        # # 芝かダートか障害か

        # In[37]:


        cource_list = race_type_list

        racetype_df = df[(df["cource"].isin(cource_list))]
        print("レースタイプ")
        # print(racetype_df)

        # # 指定騎手のオッズ指定

        # In[51]:

        print("ジョッキーオッズ")
        if target_jockey != "":
            #川田が１２倍以下のレースを抽出したデータフレーム を作成
            #６番人気が１２倍以下のレースを抽出したリスト を作成
            target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )]

            #人気馬の指定がある場合
            if win_ninki != "":

                target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )&(df["win_ninki"] ==win_ninki )]
                print("target_jockey_list")
                print(target_jockey_list)
           


            #以上、以下で場合分けできるように

            #上記データフレームのままだと、川田将雅の行しかない。
            #なので、上記データフレームのrace_IDをリスト化し、対象のrace_IDの全ての行が抽出されるようにする。

            #対象のrace_IDのリストを作成
            target_jockey_ID = target_jockey_list["race_ID"].values.tolist()

            jockey_odds_df = df[df["race_ID"].isin(target_jockey_ID)]

        else:
            jockey_odds_df = df


        # print(jockey_odds_df)

        df_list_A = [place_df, kaisai_df, distance_df,number_df,ninki_odds_df,racetype_df,jockey_odds_df]

        # # 各データフレーム を結合（共通するIDの行のみ抽出）

        df_target = pd.concat(df_list_A, axis=1, join='inner')
        
        # 重複していない列のみを抽出
        df_target = df_target.loc[:,~df_target.columns.duplicated()]
        
        #NewRaceIDのリスト化（１から連番）
        df_NewtargetID_list = df_target["NewRaceID"].values.tolist()
        print("new目印")
        print(df_NewtargetID_list)

        #重複を削るために下記の作業をする
        y = dict.fromkeys(df_NewtargetID_list)
        print(y)
        print("last目印")
        df_NewtargetID_list = list(y)
        print(df_NewtargetID_list)

        #差分を取ってレース間隔数のリスト化 
        #一回アレイに変換
        race_interval = np.array(df_NewtargetID_list)
        race_interval = np.diff(race_interval)

        print("最大レース間隔")
        max_interval = max(race_interval)
        print(max_interval)
        print("平均レース間隔")
        avg_interval = np.average(race_interval)
        print(avg_interval)

        #リストに戻す
        race_interval = list(race_interval)

        print(race_interval)

        #加工後のデータフレームのrace_IDをリスト化
        df_targetID_list = df_target["race_ID"].values.tolist()
        #リスト型を代入したdf_targetID_list内の各要素を,区切りで繋げ、１つの文字列にする。
        # print(df_targetID_list)
        
        df_targetID_list = map(str, df_targetID_list) #格納される数値を文字列にする
        
        df_targetID_list = list(df_targetID_list)
        
        print(dict.fromkeys(df_targetID_list))
        # {3: None, 2: None, 1: None, 5: None, 4: None}
        y = dict.fromkeys(df_targetID_list)
        print("目印：dict.fromkeys(df_targetID_list")
        print(y)
        l_unique_order = list(y)
        print(l_unique_order)

        print(l_unique_order)
        # [3, 2, 1, 5, 4]


        # print(df_targetID_list)
        targetID_list = ','.join(l_unique_order)

        print("目印：targetID_list")
        print(targetID_list)
        print(df_target[df_target["race_ID"].isin(df_targetID_list)].index)
        print(df_target[df_target["race_ID"].isin(df_targetID_list)])
        # obj = TargetRaceID()
        # friend = TargetRaceID(target_RaceID=targetID_list)
        # friend.save()

        print("結合")
        # print(df_target)


        # for item, row in df_target.iterrows():
        #     print(row.jockey)
       
        # obj = LogicSetting.objects.get(id=id)

        racecounts = df_target['race_ID'].nunique()
        print("確認用ボタン後、レース数")
        print(racecounts)

        #post後に登録用フォームを表示
        # recordbutton = RecordButtonForm
        recordbutton = RaceStteiForm

        ms1 ="POST後"

        request.session['form_data'] = copy.deepcopy(request.POST)
        QueryDict = request.session['form_data'] 
        print(QueryDict)
        racesettei_list = RaceSettei.objects

        record = 'style="display: block;"'
        confirm = 'style="display: none;"'
        

    else:
        form = RaceStteiForm()
        
        # logictestbutton = ''
        QueryDict = ''
        # race_place = ''
        win_ninki = ''
        win_ninki_plus =''
        # start_date = ''
        start_df = ''
        y = ''
        racecounts =''

        df_target = ''
        ms1 = "POST前"
        recordbutton = ''
        racesettei_list = RaceSettei.objects

        record = 'style="display: none;"'
        confirm = 'style="display: block;"'

        max_interval = ""
        avg_interval = ""
        


    params = {
    
    # 'logictestbutton':logictestbutton,
    'form':form,
    # 'session':request.session['form_data'],
    'QueryDict':QueryDict,
    'racecounts':racecounts,
    'df_target':df_target,
    'recordbutton':recordbutton,
    'ms1':ms1,
    'racesettei_list':racesettei_list,
    'record':record,
    'confirm':confirm,
    'max_interval':max_interval,
    'avg_interval':avg_interval,
    }
    
    return render(request,'keiba/racesettei.html',params)


# レース設定登録保存
def racerecord(request):

    if(request.method == 'POST'):

        # form = RaceStteiForm(copy.deepcopy(request.POST))
        # request.session['form_data']
        # QueryDict = request.session['form_data'] 
        # print(QueryDict)
        # print(type(QueryDict))


        # form = RaceStteiForm(request.POST)

        

        request.session['form_data'] = copy.deepcopy(request.POST)
        QueryDict = request.session['form_data'] 
        print(QueryDict)
        print(type(QueryDict))
        
        # print(QueryDict.__getitem__('logic_select'))
        
        form = RaceStteiForm(QueryDict)

        print(form)


        
        # print(race_place)
        
        #リスト型を代入したrace_place内の各要素を,区切りで繋げ、１つの文字列にする。
        # mojiretu = ','.join(race_place)
        # print(mojiretu)

        # 文字列をLogicSettingに保存する
        # LogicSetting.objects.create(race_place=mojiretu)
        
        #セッション情報から各変数に格納

        #セッション情報が入ったQueryDictから、race_placeをキーとして値をリスト型で取得
        place_list = QueryDict.getlist('race_place')

        race_place = ','.join(place_list)

        race_type_list = QueryDict.getlist('race_type')

        race_type = ','.join(race_type_list)
        
        start_date = QueryDict.__getitem__('start_date')
        end_date = QueryDict.__getitem__('end_date')


        from_distance = QueryDict.__getitem__('from_distance')
        to_distance = QueryDict.__getitem__('to_distance')

        win_ninki = QueryDict.__getitem__('win_ninki')
        if win_ninki != "":
            win_ninki = int(win_ninki)
        else:
            #空文字がstring型になったものを、integerfiledに入れるとエラーになるので、
            win_ninki = None
            print(win_ninki)
            print(type(win_ninki))
            print("目印")

        target_jockey = QueryDict.__getitem__('target_jockey')

        odds_minimum = QueryDict.__getitem__('odds_minimum')
        print(odds_minimum)
        if odds_minimum !="":
            odds_minimum = float(odds_minimum)
        else:
            odds_minimum = 1
        odds_max = QueryDict.__getitem__('odds_max')
        print(odds_max)
        if odds_max !="":
            odds_max = float(odds_max)
        else:
            odds_max = 1000

        number_horse_min = QueryDict.__getitem__('number_horse_min')
        if number_horse_min != "":
            number_horse_min= int(number_horse_min)
        else:
            number_horse_min = 1
        number_horse_max = QueryDict.__getitem__('number_horse_max')
        if number_horse_max != "":
            number_horse_max = int(number_horse_max)
        else:
            number_horse_max = 18

# レースデータの絞り込み

        # 全オブジェクトデータを取得
        racedata = RaceData.objects.all()   
       
        # データをデータフレーム化
        df = read_frame(racedata)

        
        #重複したレースIDごとに番号を付けて新しい連番を作る
        df['NewRaceID'] = pd.factorize(df['race_ID'])[0]
        #0から始まる連番を１から始める
        df['NewRaceID'] = df['NewRaceID'] +1
        print(df)




        # 開催場の絞り込み        
        place_df = df[df["race_place"].isin(place_list)]
        # print("場所")
        # print(place_df)

        # 開催日の絞り込み 
        kaisai_df = df[(df["start_date"] >= start_date)&(df["end_date"] <= end_date)]
        # print("期間")
        # print(kaisai_df)

        # # 距離抽出

        # In[54]:


        distance_df = df[(df.from_distance>=from_distance)&(df.from_distance<=to_distance)]
        # print("期間")
        # print(distance_df)

        # # 出走馬数の指定

        # In[53]:
        print("馬数")
        print(type(number_horse_min))
        number_df = df[(df["uma_number1"]>=number_horse_min)&(df["uma_number1"]<=number_horse_max)]
        
        # print(number_df)


        # # 指定人気馬のオッズ指定
        # 
        # 

        # In[52]:


        #６番人気が１２倍以下のレースを抽出したデータフレーム を作成

        #６番人気が１０倍以上１２倍以下のレースを抽出したリスト を作成
        print("人気オッズ")
        if win_ninki != None:

            ninki_odds_df = df[(df["win_ninki"] == win_ninki)&(df["from_odds"] >=odds_minimum )&(df["from_odds"] <=odds_max)]

            #以上、以下で場合分けできるように

            #上記データフレームのままだと、６番人気の行しかない。
            #なので、上記データフレームのrace_IDをリスト化し、対象のrace_IDの全ての行が抽出されるようにする。

            #対象のrace_IDのリストを作成
            raceID_list = ninki_odds_df["race_ID"].values.tolist()

            
            ninki_odds_df = df[df["race_ID"].isin(raceID_list)]
        else:
            ninki_odds_df = df
        
        print(ninki_odds_df)

        # # 芝かダートか障害か

        # In[37]:


        cource_list = race_type_list

        racetype_df = df[(df["cource"].isin(cource_list))]
        print("レースタイプ")
        print(racetype_df)

        # # 指定騎手のオッズ指定

        # In[51]:

        print("ジョッキーオッズ")
        if target_jockey != "":
            #川田が１２倍以下のレースを抽出したデータフレーム を作成
            #６番人気が１２倍以下のレースを抽出したリスト を作成
            target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )]


            #人気馬の指定がある場合
            if win_ninki != "":

                target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )&(df["win_ninki"] ==win_ninki )]
                print("target_jockey_list")
                print(target_jockey_list)


            #以上、以下で場合分けできるように

            #上記データフレームのままだと、川田将雅の行しかない。
            #なので、上記データフレームのrace_IDをリスト化し、対象のrace_IDの全ての行が抽出されるようにする。

            #対象のrace_IDのリストを作成
            target_jockey_ID = target_jockey_list["race_ID"].values.tolist()

            jockey_odds_df = df[df["race_ID"].isin(target_jockey_ID)]

        else:
            jockey_odds_df = df


        # print(jockey_odds_df)

        df_list_A = [place_df, kaisai_df, distance_df,number_df,ninki_odds_df,racetype_df,jockey_odds_df]

        # # 各データフレーム を結合（共通するIDの行のみ抽出）

        df_target = pd.concat(df_list_A, axis=1, join='inner')
        # 重複していない列のみを抽出
        df_target = df_target.loc[:,~df_target.columns.duplicated()]


        #NewRaceIDのリスト化（１から連番）
        df_NewtargetID_list = df_target["NewRaceID"].values.tolist()
        print("new目印")
        print(df_NewtargetID_list)

        #重複を削るために下記の作業をする
        y = dict.fromkeys(df_NewtargetID_list)
        print(y)
        print("last目印")
        df_NewtargetID_list = list(y)
        print(df_NewtargetID_list)

        #差分を取ってレース間隔数のリスト化 
        #一回アレイに変換
        race_interval = np.array(df_NewtargetID_list)
        race_interval = np.diff(race_interval)

        print("最大レース間隔")
        max_interval = max(race_interval)
        print(max_interval)
        print("平均レース間隔")
        avg_interval = np.average(race_interval)
        print(avg_interval)

        #リストに戻す
        race_interval = list(race_interval)

        print(race_interval)   





        
        #加工後のデータフレームのrace_IDをリスト化
        df_targetID_list = df_target["race_ID"].values.tolist()
        #リスト型を代入したdf_targetID_list内の各要素を,区切りで繋げ、１つの文字列にする。
        # print(df_targetID_list)
        
        df_targetID_list = map(str, df_targetID_list) #格納される数値を文字列にする
        
        df_targetID_list = list(df_targetID_list)
        
        print(dict.fromkeys(df_targetID_list))
        # {3: None, 2: None, 1: None, 5: None, 4: None}
        y = dict.fromkeys(df_targetID_list)
        l_unique_order = list(y)

        print(l_unique_order)
        # [3, 2, 1, 5, 4]


        # print(df_targetID_list)
        targetID_list = ','.join(l_unique_order)


        print(targetID_list)

        obj = TargetRaceID()
        friend = TargetRaceID(target_RaceID=targetID_list)
        friend.save()
        
        print("結合")
        # print(df_target)


        # for item, row in df_target.iterrows():
        #     print(row.jockey)
       
        # obj = LogicSetting.objects.get(id=id)

        racecounts = df_target['race_ID'].nunique()

        howmany_race = racecounts
        print("レース数目印")
        print(howmany_race)


        #post後に登録用フォームを表示
        # recordbutton = RecordButtonForm
        recordbutton = RaceStteiForm

        ms1 ="POST後"

        request.session['form_data'] = copy.deepcopy(request.POST)
        QueryDict = request.session['form_data'] 
        print(QueryDict)
        racesettei_list = RaceSettei.objects
        

        obj = RaceSettei()
        friend = RaceSettei(race_place=race_place,race_type=race_type,start_date=start_date,\
                           end_date=end_date,from_distance=from_distance,to_distance=to_distance,\
                           number_horse_min=number_horse_min,number_horse_max=number_horse_max,\
                           win_ninki=win_ninki,target_jockey=target_jockey,odds_minimum=odds_minimum,\
                           odds_max=odds_max,howmany_race=howmany_race,max_interval=max_interval,avg_interval=avg_interval)
        friend.save()



    else:
        form = RaceStteiForm()
        # request.session['form_data']
        print(request.session['form_data'])

    params= { 
        'title':'登録しました',
        'session2':request.session['form_data'],
    }

    return render(request, 'keiba/racerecord.html',params)
            

  