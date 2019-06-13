from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.views.generic import TemplateView
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.db.models import Q
# from django.contrib.auth.mixin import LoginRequiredMixin
# from .oricalc import simplecalc


# from .martingale_m import martingale

from .forms import LogicTestForm,RaceStteiForm, LogicForm,RaceRecordForm,RaceRecordForm,RecordButtonForm,LogicRecordForm,logiclist,LogicLoadForm

from .models import  RaceData,TargetRaceData,TargetRaceID,RaceSettei,Logic

from django_pandas.io import read_frame
import pandas as pd
import numpy as np
# 
from datetime import datetime as dt

from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



from .forms import UserForm


# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

import copy


import openpyxl
# import xlsxwriter
import numpy as np
import datetime as dt

from .import bet_algo
from . bet_algo import Logics

import importlib
importlib.reload(bet_algo)
import json





def __new_str__(self):
    result = ''
    for item in self:
        result += '<tr>'
        for k in item:
            result += '<td>'+str(k)+ '=' + str(item[k])+'</td>'
        result += '</tr>'
    return result

QuerySet.__str__ = __new_str__


def index(request):
    
    # params = {
    #     'title':'モード選択画面'
    #     }
    return render(request, 'keiba/index.html')


def create_user_view(request):
    form = UserForm()
    return render(request,'create_user_view.html',{'form':form})






# def login(request):
#     user = authenticate(
#         username=request.POST.get('username'),
#         password=request.POST.get('password')
#     )
#     login(request,user)
#     return render(request,'index.html')

def login_view(request):
    user = authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )
    login(request,user)
    return redirect('/')


def create_user(request):
    user = User.objects.create_user(
        request.POST.get('username'),
        request.POST.get('email'),
        request.POST.get('password')
    )

    user.save()
    return redirect('/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')



def home(request):

    
    params = {
        'title':'ホーム画面',
        }
    return render(request, 'keiba/home.html', params)

def forquestion(request):

    
    params = {
        'title':'テスト',
        }
    return render(request, 'keiba/forquestion.html', params)


def session_count(request):
    if 'count' in request.session:
        request.session['count'] += 1
    else:
        request.session['count'] = 0
    
    return HttpResponse(str(request.session['count']))

def session_flush(request):
    request.session.flush()
    return redirect(to='/keiba/session_count')





def logic(request):


    is_post = False
    csrf_list = []

    if 'is_post' in request.session:
        is_post = request.session['is_post']

    # csrf_list が session になければ、空文字定義
    if 'csrf_list' not in request.session or request.session['csrf_list'] is None:
        request.session['csrf_list'] = ''

    # &で区切られているので、それを区切り文字に配列を作る
    csrf_list = request.session['csrf_list'].split('&')

    #読み込みボタン（csrfmiddlewaretokenが新しく追加）を押した場合
    if request.method == 'POST' and request.POST['csrfmiddlewaretoken'] not in csrf_list:
        is_post = False
    elif request.method == 'POST':
        is_post = True

    # csrfmiddlewaretoken がポストデータにあれば、追加する
    
    #読み込みボタン（csrfmiddlewaretokenが新しく追加）を押した場合
    if request.method == 'POST' and 'csrfmiddlewaretoken' in request.POST and request.POST['csrfmiddlewaretoken'] not in csrf_list:
        csrf_list.append(request.POST['csrfmiddlewaretoken'])

    # session の csrf_list に追加
    request.session['csrf_list'] = '&'.join(csrf_list)


    if request.method == 'POST' and not is_post:
        request.session['is_post'] = True

        if 'button_1' in request.POST:
            budget = 50000


        form = LogicForm(request.POST)

        form2 = logiclist(request.POST)

        request.session['form_data'] = request.POST
        QueryDict = request.session['form_data'] 
        print("logicポスト後")
       

        logic_id = QueryDict.__getitem__('logiclist')

        obj = Logic.objects.get(id=logic_id)

        target_race = obj.target_race
        
        budget = obj.budget
        loaded_budget = obj.budget

        initial_bet = obj.initial_bet
        select_or_manual = obj.select_or_manual
        
        bet_way = obj.bet_way
        fix_or_variable = obj.fix_or_variable
        fix_bet = obj.fix_bet

        reset_when_hit = obj.reset_when_hit
        
        lost_bet_reset = obj.lost_bet_reset
        win_bet_reset = obj.win_bet_reset
        stopbet_bylost = obj.stopbet_bylost
        stopbet_bymaxbet = obj.stopbet_bymaxbet

        stop_when_hit = obj.stop_when_hit
        target_ninki = obj.target_ninki
        target_jockey = obj.target_jockey
        odds_minimum = obj.odds_minimum
        odds_max = obj.odds_max


        countdown_select = obj.countdown_select
        countdown_ninki = obj.countdown_ninki
        countdown_jockey = obj.countdown_jockey

        start_bet_ninki = obj.start_bet_ninki
        start_bet_jockey = obj.start_bet_jockey
        target_place = obj.target_place

        win_bet_select = obj.countdown_select
        margin = obj.margin

        if margin:
            margin = float(margin)

        # #登録する
        # obj = Logic()
        # friend = LogicRecordForm(request.POST, instance=obj)
        # friend.save()

        if countdown_ninki != "":
            countdown_ms1 = "{0}番人気が{1}回以上{2}着外でベット開始".format(countdown_ninki, start_bet_ninki, target_place)
        else:
            countdown_ms1 = ""

        if countdown_jockey != "":
            countdown_ms2 = "{0}が{1}回以上{2}着外でベット開始".format(countdown_jockey,start_bet_ninki,target_place)
        else:
            countdown_ms2 = ""

        ms1 ="POST後"

        logic_id = obj.id

        logic_list = Logic.objects
        logiclistform = logiclist(initial={'logiclist':logic_id})
        form = LogicForm(initial={
            'target_race': target_race,
            'budget': budget,
            'loaded_budget': loaded_budget,
            'initial_bet': initial_bet,
            'select_or_manual': select_or_manual,
            'bet_way': bet_way,
            'fix_or_variable': fix_or_variable,
            'fix_bet': fix_bet,
            'reset_when_hit': reset_when_hit,
            'lost_bet_reset': lost_bet_reset,
            'win_bet_reset': win_bet_reset,
            'stopbet_bylost': stopbet_bylost,
            'stopbet_bymaxbet': stopbet_bymaxbet,
            'stop_when_hit': stop_when_hit,
            'win_bet_select':win_bet_select,
            'target_ninki': target_ninki,
            'target_jockey': target_jockey,
            'odds_minimum': odds_minimum,
            'odds_max': odds_max,
            'countdown_select': countdown_select,
            'countdown_ninki': countdown_ninki,
            'countdown_jockey': countdown_jockey,
            'start_bet_ninki': start_bet_ninki,
            'start_bet_jockey': start_bet_jockey,
            'target_place': target_place,
            'margin': margin,
            })
    else:
        request.session['is_post'] = False

        logiclistform = logiclist()
        form = LogicForm()
        countdown_ms1 =""
        countdown_ms2 =""
        ms1 = "POST前"
        logic_list = Logic.objects
        loaded_budget = ""


    params = {
        'ms1':ms1,
        'logiclistform':logiclistform,
        'form':form,
        'countdown_ms1':countdown_ms1,
        'countdown_ms2':countdown_ms2,
        'logic_list' : logic_list,
        'loaded_budget':loaded_budget,
    }


    return render(request, 'keiba/logic.html', params)


def result(request):
    if(request.method == 'POST'):

        race_list_whenbet = []
        revenue_list = []
        bet_losing_streak = 0   
        target_place_ninki_list = []
        target_ninki_odds = []




        # request.session['form_data'] = request.POST

        # querydict をmutable(後で変更）するため、copy()としている
        request.session['form_data'] = request.POST.copy()
        request.session['form_data']
        # セッションデータをQueryDictという変数に格納
        QueryDict = request.session['form_data']

        form =""
        
        # 全オブジェクトデータを取得
        racedata = RaceData.objects.all()   
       
        # データをデータフレーム化
        df = read_frame(racedata)
        
        #重複したレースIDごとに番号を付けて新しい連番を作る(ex. 0,1,2,3.....)
        df['NewRaceID'] = pd.factorize(df['race_ID'])[0]
        #0から始まる連番を１から始める
        df['NewRaceID'] = df['NewRaceID'] +1
        # print(df)
       
        #全レースを連番をリスト化
        NewRaceID_list = list(df.NewRaceID.unique())

        # #着順が１着の行のみを抽出（同率一位の場合は後で検討）
        # place_one_df = df[(df['place_number']==1)].loc[:, ["race_place","race_number","win_ninki","from_odds","win_return"]]

        #フォーム上のターゲットレースから選択した値を代入
        target_race = QueryDict.__getitem__('target_race')

        # 選択したレースIDのTargetRaceIDオブジェクトを生成
        obj = TargetRaceID.objects.get(id=target_race)

        # 上記オブジェクトのtarget_RaceID(複数のレースIDがカンマ区切りで入っている）を値を代入
        target_raceID = obj.target_RaceID
        
        # target_RaceIDをカンマを区切りにして、リストとする。(ex.201706010101,201706010102.....)
        target_raceID_list = [x.strip() for x in target_raceID.split(',')]

        # dfの中から、新しいデータフレーム （target_df）を作成。      
        target_df = df[df["race_ID"].isin(target_raceID_list)]

        # target_dfのNewRaceIDをリスト化する。（ex.1,1,1,1,1,1,1,1,1,3,3,3...)
        target_NewRaceID_list =target_df['NewRaceID'].values.tolist()

        # 重複を削除
        #空のリストを作成
        target_NewRaceID_list_unique = []
        for i in target_NewRaceID_list:
            if i not in target_NewRaceID_list_unique:
                target_NewRaceID_list_unique.append(i)
        
        print("ターゲットレースID(連番）",target_NewRaceID_list_unique)

        # #着順が１着の行のみを抽出（同率一位の場合は後で検討）
        # new_df = target_df[(target_df['place_number']==1)].loc[:, ["race_place","race_number","win_ninki","from_odds","win_return"]]
        
        # #着順が１着の行のみデータフレーム から、その人気の値をリストとして抽出
        # target_list_ninki = new_df["win_ninki"].values.tolist()
        # target_list_return = new_df["win_return"].values.tolist()


        budget = QueryDict.__getitem__('budget')
        budget = int(budget)
        
        initial_bet = QueryDict.__getitem__('initial_bet')
        initial_bet = int(initial_bet)
        
        stopbet_bymaxbet = QueryDict.__getitem__('stopbet_bymaxbet')
        if stopbet_bymaxbet != "":
            stopbet_bymaxbet = int(stopbet_bymaxbet)
        else:
            stopbet_bymaxbet = 10000000000000000 
        
        # disableでセッションの辞書にキーが入っていない場合にエラーにならないように場合分け
        if 'bet_way' in QueryDict.keys():
            bet_way = QueryDict.__getitem__('bet_way')
        else:
            bet_way = ""

        # fix_or_variable = QueryDict.__getitem__('fix_or_variable')
        # if 'fix_bet' in QueryDict.keys():
        #     fix_bet = QueryDict.__getitem__('fix_bet')
        # else:
        #     fix_bet =""
        # if 'reset_when_hit' in QueryDict.keys():
        #     reset_when_hit = QueryDict.__getitem__('reset_when_hit')
        # else:
        #     reset_when_hit = ""

        
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
        # target_jockey = QueryDict.__getitem__('target_jockey')
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
        if countdown_ninki != "":
            countdown_ninki = int(countdown_ninki)
        else:
            countdown_ninki = ""

        # countdown_jockey = QueryDict.__getitem__('countdown_jockey')

        start_bet_ninki = QueryDict.__getitem__('start_bet_ninki')
        if start_bet_ninki !="":
            start_bet_ninki = int(start_bet_ninki)
        else:
            start_bet_ninki =""
        
        # start_bet_jockey = QueryDict.__getitem__('start_bet_jockey')
        # win_bet_select = QueryDict.__getitem__('win_bet_select')
        
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
            countdown_ms1 = str(countdown_ninki)+"番人気が"+str(start_bet_ninki)+"回以上"+str(target_place)+"着外でベット開始"
        else:
            countdown_ms1 =""
        # if countdown_jockey != "":
        #     countdown_ms2 = countdown_jockey+"が"+str(start_bet_ninki)+"回以上"+str(target_place)+"着外でベット開始"
        # else:
        #     countdown_ms2 =""

        margin = QueryDict.__getitem__('margin')
        # marginに値がある場合のみ、floatに変換(これをしないとstring("")からfloatにできないというエラーが発生してしまう)
        if margin:
            margin = float(margin)


         #着順が１着の行のみを抽出（同率一位の場合は後で検討）
        place_one_target_df = target_df[(target_df['place_number']==1)].loc[:, ["race_place","race_number","win_ninki","from_odds","win_return"]]

        #着順が１着の行のみデータフレーム から、その人気の値をリストとして抽出
        win_ninki_list = place_one_target_df["win_ninki"].values.tolist()
        #着順が１着の行のみデータフレーム から、その払い戻しをリストとして抽出
        win_return_list = place_one_target_df["win_return"].values.tolist()

        # print(NewRaceID_list)
        print(win_ninki_list)
        print(win_return_list)
        print(NewRaceID_list)
        #着順がtarget_place着以内の行のみデータフレーム から、その人気をリストとし抽出

        #対象人気が含まれるレースのNewRaceIDをリスト化(対象人気がないレースに"なし"を入れるため)
        #対象人気のレースが含まれるレースのIDをリスト化
        target_ninki_NewRaceID_list = target_df[target_df["win_ninki"]==target_ninki].NewRaceID.values.tolist()
        

        #対象着順以内のリストを作成。
        for i in target_NewRaceID_list_unique:
            # print("レース番号",i)
            target_place_ninki_list.append(target_df[(target_df.NewRaceID==i)&(target_df.place_number<=target_place)&(target_df.place_number >=1)].sort_values('place_number').win_ninki.values.tolist()[0:len(range(target_place))])
        
        #ターゲット人気のオッズリストを作成
        for i in target_NewRaceID_list_unique:
            if i in target_ninki_NewRaceID_list:

                target_ninki_odds.append(target_df[(target_df.NewRaceID==i)&(target_df.win_ninki==target_ninki)].from_odds.values.tolist()[0])

            else:
                target_ninki_odds.append("なし")

        print("target_place_ninki_list",target_place_ninki_list)
        print("target_ninki_odds",target_ninki_odds)

        print("target_ninki_oddsの要素数",len(target_ninki_odds))
        print("target_ninki_NewRaceID_listの要素数",len(target_ninki_NewRaceID_list))
        print("target_NewRaceID_list_uniqueの要素数",len(target_NewRaceID_list_unique))




        # Logicsクラスからオブジェクトを生成
        # 注意！引数を追加したら、bet_logicのdef __init__()にも引数を同じ順番で追加すること
        betman = Logics(start_bet_ninki,NewRaceID_list,budget,odds_minimum,odds_max,target_df\
                ,initial_bet,stopbet_bylost,stopbet_bymaxbet,stop_bymaxprofit\
                ,countdown_ninki,target_place,target_ninki,margin,target_NewRaceID_list_unique\
                ,place_one_target_df,win_ninki_list,win_return_list,target_ninki_NewRaceID_list\
                ,target_place_ninki_list,target_ninki_odds)



        # if bet_way =='マーチンゲール' and countdown_select=='人気':
        if bet_way =='マーチンゲール':

            bet_losing_streak_list,list_empty,maxlost_list,race_list_whenbet,\
            profit_list,bet_list,revenue_list,race_renban_list,win_ninki_list,reason_for_stop = betman.martingale_countdown_ninki()

            # return mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet, profit_result, recovery_rate,race_list_whenbet

        # if bet_way =='マーチンゲール' and countdown_select=='ジョッキー':

        #     mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet, profit_result, recovery_rate,race_list_whenbet = betman.martingale_countdown_jockey()

        #     return mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet, profit_result, recovery_rate,race_list_whenbet

        # if bet_way =='利益率確定法' and countdown_select == '人気':
        if bet_way =='利益率確定法':
            bet_losing_streak_list,list_empty,maxlost_list,race_list_whenbet,\
            profit_list,bet_list,revenue_list,race_renban_list,win_ninki_list,reason_for_stop = betman.margin_fix_ninki()

            # return mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet, profit_result, recovery_rate,race_list_whenbet

        # if bet_way =='利益率確定法' and countdown_select == 'ジョッキー':

        #     mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet, profit_result, recovery_rate,race_list_whenbet = betman.margin_fix_jockey()
    
        # if select_or_manual == 'マニュアル' and countdown_ninki == '人気':

        #     mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet, profit_result, recovery_rate,race_list_whenbet = betman.manual()

        


        # print(betman.martingale())
        print("マーチンゲール 引数チェック")
        print("budget",budget)
        print("initial_bet",initial_bet)  
        print("odds_minimum",odds_minimum) 


        
       
        print("bet_list",bet_list)
        # bet_list,bet_losing_streak_list,revenue_list,maxlost_list,list_empty,profit_list = martingale(budget,initial_bet,select_or_manual,fix_or_variable,fix_bet,reset_when_hit,lost_bet_reset,win_bet_reset,stopbet_bylost,target_ninki,odds_minimum,odds_max,countdown_ninki,countdown_jockey,start_bet_ninki,start_bet_jockey,target_ninki,target_place)
        print("race_list_whenbet",race_list_whenbet)


        # print(target_list_ninki)


        recordbutton = RecordButtonForm


        ms = "POST後"

        
        ##### 集計
        print("race_renban_list",race_renban_list)
        print(len(race_renban_list))

        # 対象人気の連敗数を計算
        renpai_list = []
        renpai = 0

        #indexの連番を振り直す
        target_df = target_df.reset_index()
        target_df['newrenban'] = target_df.index.values
        renban_list = target_df['newrenban'].values.tolist()  

        renban_list.insert(0,0)
        renban_list.pop(-1) 

        # NewRaceIDはレース全体の連番IDの中からtarget_dfに該当する連番のリスト

        all_place_ninki_list = []
       
        for i in target_NewRaceID_list_unique:
            ninki_list = target_df[target_df.NewRaceID==i].sort_values('place_number').win_ninki.values.tolist()
            if 0 in ninki_list:
                ninki_list.remove(0)
            all_place_ninki_list.append(ninki_list)


        for i in range(len(target_raceID_list)):
            if i == len(target_raceID_list)-1:
                renpai_list.append(renpai)

            elif target_ninki not in all_place_ninki_list[i]:
                # print(target_ninki,"は",i,"レースにいないのでスキップ")
                continue
            elif win_ninki_list[i] == target_ninki:
                # print(i,"レース目１着")
                renpai_list.append(renpai)
                renpai = 0

            else:
                # print("外れ")
                renpai += 1



        #レース間隔を計算
         
        #一回アレイに変換
        race_interval_logic = np.array(race_list_whenbet)
        #差分を取ってレース間隔数のリスト化
        race_interval_logic = np.diff(race_interval_logic)

        print("最大レース間隔")
        max_interval = max(race_interval_logic)
        print(max_interval)
        print("平均レース間隔")
        avg_interval = np.average(race_interval_logic)
        print(avg_interval)

        #リストに戻す
        race_interval_logic = list(race_interval_logic)

        print(race_interval_logic)

        mxlost = max(bet_losing_streak_list,default=0)
        print("最大不的中数",mxlost)
        print(list_empty)
        mx = max(renpai_list,default=0)
        print("最大連敗数",mx)
        print(maxlost_list)
        mx_loss =max(maxlost_list,default=0)
        print("最大損失額",mx_loss,"円")

        print("ベット対象レースリスト",race_list_whenbet)
        print("的中時利益：",profit_list)
        print("的中時利益合計:",sum(profit_list))
        profit_sum = sum(profit_list)
        print("ベット金額合計:",sum(bet_list))
        bet_sum = sum(bet_list)

        mxbet = max(bet_list,default=0)
        print("最高ベット金額",mxbet)
        print("払戻合計:",sum(revenue_list))
        return_sum = sum(revenue_list)

        



        count_bet = len(bet_list)

                # 回収率
        if bet_sum != 0 or return_sum != 0:
            recovery_rate = (return_sum / bet_sum) * 100
        else:
            recovery_rate = 0

        #小数点第２位未満を四捨五入
        recovery_rate = round(recovery_rate,2)
        avg_interval = round(avg_interval,2)



        

        #利益
        profit_result = return_sum - bet_sum

        intlist = [mxlost,mx,mx_loss,profit_sum,bet_sum,return_sum,count_bet,profit_result,max_interval]




        # numpy.int64のままだとエラーになるので、int型に変換

        # mxlost,mx,mx_loss,profit_sum,bet_sum,return_sum,count_bet,profit_result,max_interval = [int(x) for x in intlist]
        # なぜか上記の式だとエラーになるので、map関数を使う

        intlist = map(int,intlist)

        # アンパック
        mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, count_bet, profit_result, max_interval = intlist

        data = [mxlost,mx,mx_loss, profit_sum, bet_sum, return_sum, bet_list,count_bet,profit_result,recovery_rate,race_list_whenbet,max_interval,avg_interval,mxbet]


        d = {'mxlost':mxlost,'mx':mx,'mx_loss':mx_loss,
             'profit_sum':profit_sum,'bet_sum':bet_sum,'return_sum':return_sum,
             'count_bet':count_bet,'profit':profit_result,'recovery_rate':recovery_rate,
             'max_interval':max_interval,'avg_interval':avg_interval,'mxbet':mxbet,"reason_for_stop":reason_for_stop}

        QueryDict.update(d)
        request.session['form_data'] = QueryDict

        
    

    else:
        ms = "POST前"
        form = "",
        countdown_ms1 ="",
        countdown_ms2 ="",
        QueryDict = "",
        target_df = "",
        data = [],
        NewRaceID_list = [],

    params = {
        'ms':ms,
        'form':form,
        'countdown_ms1':countdown_ms1,
        # 'countdown_ms2':countdown_ms2,
        'QueryDict':QueryDict,
        'target_df':target_df,
        'data':data,
        'NewRaceID_list':NewRaceID_list,
    }


    return render(request, 'keiba/result.html', params)


def logic_save(request):

    #Logicに保存
    # print(request.session['form_data'])
    # request.session['form_data'] = request.POST
    obj = Logic()


    friend = LogicRecordForm(request.session['form_data'], instance=obj)


    friend.save()
    # x = request.session['form_data']
    # print(type(x))
    # print(x.get('budget'))
    #
    # target_race = x.get('target_race')
    #
    # budget = x.get('budget')
    #
    # initial_bet = x.get('initial_bet')
    #
    # # ベット方法から選択するか、マニュアルかの選択
    # select_or_manual = x.get('select_or_manual')
    #
    # bet_way = x.get('bet_way')
    #
    # # 定額か変動額かの選択
    # fix_or_variable = x.get('fix_or_variable')
    # fix_bet = x.get('fix_bet')
    #
    # nanbai = x.get('nanbai')
    #
    # reset_when_hit = x.get('reset_when_hit')
    # lost_bet_reset = x.get('lost_bet_reset')
    # # 的中ではなく一着であることに注意
    #
    # win_bet_reset = x.get('win_bet_reset')
    # stopbet_bylost = x.get('stopbet_bylost')
    # stopbet_bymaxbet = x.get('stopbet_bymaxbet')
    # stop_when_hit = x.get('stop_when_hit')
    #
    # stop_bymaxprofit = x.get('stop_bymaxprofit')
    #
    # # 対象買い目の選択
    # target_ninki = x.get('target_ninki')
    # target_jockey = x.get('target_jockey')
    #
    # odds_minimum = x.get('odds_minimum')
    # odds_max = x.get('odds_max')
    #
    # countdown_select = x.get('countdown_select')
    #
    # countdown_ninki = x.get('countdown_ninki')
    # countdown_jockey = x.get('countdown_jockey')
    #
    # start_bet_ninki = x.get('start_bet_ninki')
    # start_bet_jockey = x.get('start_bet_jockey')
    # target_place = x.get('target_place')
    #
    # margin = x.get('margin')
    #
    # # 成績登録用
    #
    # # data = [mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list, count_bet, profit_result, recovery_rate,
    # #         race_list_whenbet, max_interval, avg_interval]
    # #
    # # mxlost = data[0]
    # # mx = data[1]
    # # mx_loss = data[2]
    # # profit_sum = data[3]
    # # bet_sum = data[4]
    # # return_sum = data[5]
    # # count_bet = data[8]
    # # profit = data[9]
    # # recovery_rate = data[10]
    # # max_interval = data[12]
    # # avg_interval = data[13]
    #
    # # obj = Logic()
    # friend = Logic(target_race=target_race,budget=budget,mxlost=mxlost)
    # friend.save()








    # friend.save()

    # obj = RaceSettei()
    # friend = RaceSettei(race_place=race_place, race_type=race_type, start_date=start_date, \
    #                     end_date=end_date, from_distance=from_distance, to_distance=to_distance, \
    #                     number_horse_min=number_horse_min, number_horse_max=number_horse_max, \
    #                     win_ninki=win_ninki, target_jockey=target_jockey, odds_minimum=odds_minimum, \
    #                     odds_max=odds_max, howmany_race=howmany_race, max_interval=max_interval,
    #                     avg_interval=avg_interval)
    # friend.save()



    
    ms1 = '登録しました！'

    params = {
        'ms1':ms1,
        # 'countdown_ms2':countdown_ms2,
        # 'QueryDict':QueryDict,
        # 'new_df':new_df,
        # 'data':data,
    }

    return render(request, 'keiba/logic_save.html', params)




# def logicedit(request, num):

#     obj = Logic.objects.get(id=num)
#     if (request.method == 'POST'):
#         friend = LogicForm(request.POST, instance=obj)
#         friend.save()
#         return redirect(to='/keiba/logic')
#     params = {
#         #'datacount':datacount,
#         'title':'Hello',
#         'id':num,
#         'form':LogicForm(instance=obj)
#     }
#     return render(request, 'keiba/logicedit.html',params)










def racesettei(request):
    if(request.method == 'POST'):

        form = RaceStteiForm(request.POST)

        

        request.session['form_data'] = copy.deepcopy(request.POST)
        QueryDict = request.session['form_data'] 
        print(QueryDict)
        print(type(QueryDict))

        # race_id = [[x.id, x.id] for x in TargetRaceID.objects.all()]
        
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
            else:
                target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )]
           


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
        # targetrace_list = TargetRaceData.objects

        record = 'style="display: block;"'
        confirm = 'style="display: none;"'
        

    else:
        form = RaceStteiForm()
        # race_id = [[x.id, x.id] for x in TargetRaceID.objects.all()]
        
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
    # 'race_id':race_id,
    # 'targetrace_list':targetrace_list,
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
        print("人気オッズ")
        if win_ninki != None:

            ninkiodds_list = df[(df["win_ninki"] == win_ninki)&(df["from_odds"] >=odds_minimum )&(df["from_odds"] <=odds_max)]

            #以上、以下で場合分けできるように

            #上記データフレームのままだと、６番人気の行しかない。
            #なので、上記データフレームのrace_IDをリスト化し、対象のrace_IDの全ての行が抽出されるようにする。

            #対象のrace_IDのリストを作成
            raceID_list = ninkiodds_list["race_ID"].values.tolist()

            
            ninki_odds_df = df[df["race_ID"].isin(raceID_list)]
        else:
            
            ninkiodds_list = df[(df["from_odds"] >=odds_minimum )&(df["from_odds"] <=odds_max)]
        
            raceID_list = ninkiodds_list["race_ID"].values.tolist()

            ninki_odds_df = df[df["race_ID"].isin(raceID_list)]
        
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
            target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )]

            #人気馬の指定がある場合
            if win_ninki != None:

                target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )&(df["win_ninki"] ==win_ninki )]
                print("target_jockey_list")
                print(target_jockey_list)
            else:
                target_jockey_list = df[(df["jockey"] == target_jockey)&(df["from_odds"] >=odds_minimum)&(df["from_odds"] <=odds_max )]
           


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


        # for item, row in df_target.iterrows():
        #     print(row.jockey)
       
        # obj = LogicSetting.objects.get(id=id)



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

    
def logic_list(request):


    ms = "ロジック一覧"
    logic_list = Logic.objects
    print("logic_list",logic_list)
    logiclistform = logiclist()


    params = {
    'logiclistform':logiclistform,
    'logic_list' : logic_list,
    'ms':ms,
        }



    return render(request, 'keiba/logic_list.html',params)



            

  
def logic_load(request):
    if(request.method == 'POST'):
        # form = LogicForm(request.POST)
        # form = Lo
        form2 = logiclist()
        # form2 = LogicForm(request.POST)

        request.session['form_data'] = request.POST
        QueryDict = request.session['form_data']
        print("logicポスト後2")
        print(QueryDict)

        logic_id = QueryDict.__getitem__('logiclist')

        obj = Logic.objects.get(id=logic_id)


        # print(obj.budget)
        
        #モデルからの読み込み
        loaded_budget = obj.budget
        loaded_target_race = obj.target_race
        loaded_initial_bet = obj.initial_bet
        loaded_select_or_manual = obj.select_or_manual
        loaded_bet_way = obj.bet_way
        loaded_fix_bet = obj.fix_bet
        loaded_nanbai = obj.nanbai
        loaded_reset_when_hit = obj.reset_when_hit
        loaded_lost_bet_reset = obj.lost_bet_reset
        loaded_stopbet_bylost = obj.stopbet_bylost
        loaded_stopbet_bymaxbet = obj.stopbet_bymaxbet
        loaded_stop_when_hit = obj.stop_when_hit
        loaded_stop_bymaxprofit = obj.stop_bymaxprofit
        loaded_target_ninki = obj.target_ninki
        loaded_target_jockey = obj.target_jockey
        loaded_odds_minimum = obj.odds_minimum
        loaded_odds_max = obj.odds_max
        loaded_countdown_select = obj.countdown_select
        loaded_countdown_ninki = obj.countdown_ninki
        loaded_countdown_jockey = obj.countdown_jockey

        loaded_start_bet_ninki = obj.start_bet_ninki
        loaded_start_bet_jockey = obj.start_bet_jockey
        loaded_target_place = obj.target_place
        loaded_margin = obj.margin
        logicloadbutton = LogicLoadForm()

    else:
        loaded_budget = ''
        #
        # form = logiclist()
        form2 = LogicForm()

        ms1 = "POST前"
        logic_list = Logic.objects

    params = {
        #
        # 'form': form,
        'form2':form2,
        'loaded_budget':loaded_budget,
        'logiclist': logiclist,
    }

    return render(request, 'keiba/logic.html', params)

        # raceID = obj.target_RaceID




    
