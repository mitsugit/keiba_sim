
# coding: utf-8

# In[1]:


import pandas as pd
import openpyxl
# import xlsxwriter
import numpy as np
import datetime as dt
import math

#エクセルファイルの読み込み
excel = pd.ExcelFile("test_df.xlsx")
#データフレーム 化
df = excel.parse(sheet_name="matome")


# In[2]:


race_ID_list = list(df.race_ID.unique())


# In[3]:


if 5 in list(df[df["race_ID"]==201706010103].win_ninki.values):
    print("いる")


# In[4]:


df['NewRaceID'] = pd.factorize(df['race_ID'])[0]


# In[5]:


df['NewRaceID'] = df['NewRaceID'] +1


# In[6]:


list(set(list(df.NewRaceID)))


# In[7]:


#全レースを連番をリスト化
NewRaceID_list = list(df.NewRaceID.unique())
#またはNewRaceID_list = list(set(list(df.NewRaceID))
NewRaceID_list


# In[8]:


mm = 3333/2
mm


# In[40]:


#追加項目


margin = 1.2

bet_reset = 0

first_bet = 0

revenue_win = 0

target_jockey = "なし"

bet = 100



target_df = df

#変数を扱いやすくする
#外部変数
initial_bet = 100
stopbet_bylost = 100000
stopbet_bymaxbet   =  50000
stop_bymaxprofit  =  30000
countdown_ninki =    1
target_place  =  3
target_ninki = 1
budget =  20000
odds_minimum = 2 
odds_max =  40
start_bet_ninki = 2

NewRaceID_list = NewRaceID_list


#クラス属性
onbet=0 
winning_streak=0 
losing_streak=0 

bet_list=[]
race_list_whenbet=[]
revenue_list=[] 
bet_losing_streak=0 
total_bet=0
bet_losing_streak_list=[]
list_empty=[]
maxlost_list=[]
profit_list=[]

target_place_ninki_list=[]
target_ninki_odds=[]



print("ベットリスト",bet_list)





# jockey_winning_streak = self.jockey_winning_streak
# jockey_losing_streak = self.jockey_losing_streak

# target_place_jockey_list = self.target_place_jockey_list
target_jockey_odds = []
target_jockey_ninki = []



print("騎手チェック")
print(target_jockey)
# print(countdown_jockey)
# print(start_bet_jockey)



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
target_ninki_NewRaceID_list = target_df[target_df["win_ninki"]==target_ninki].NewRaceID.values.tolist()
target_ninki_NewRaceID_list

#対象着順以内のリストを作成。

for i in NewRaceID_list:
    # print("レース番号",i)
    target_place_ninki_list.append(target_df[(target_df.NewRaceID==i)&(target_df.place_number<=target_place)&(target_df.place_number >=1)].sort_values('place_number').win_ninki.values.tolist()[0:len(range(target_place))])


#ターゲット人気のオッズリストを作成
for i in NewRaceID_list:
    if i in target_ninki_NewRaceID_list:

        target_ninki_odds.append(target_df[(target_df.NewRaceID==i)&(target_df.win_ninki==target_ninki)].from_odds.values.tolist()[0])

    else:
        target_ninki_odds.append("なし")

print("target_place_ninki_list",target_place_ninki_list)
print("target_ninki_odds",target_ninki_odds)
print(len(target_ninki_odds))



#対象騎手が含まれるレースのNewRaceIDをリスト化(対象人気がないレースに"なし"を入れるため)
target_jockey_NewRaceID_list = target_df[target_df["jockey"]==target_jockey].NewRaceID.values.tolist()
target_jockey_NewRaceID_list


#ターゲット騎手のオッズリストを作成

for i in NewRaceID_list:
    if i in target_jockey_NewRaceID_list:

        # print("騎手のチェック")
        # print(type(target_df[(target_df.NewRaceID==i)].jockey))
        # print(target_df[(target_df.NewRaceID==i)].jockey)
        # print(target_jockey)

        target_jockey_odds.append(target_df[(target_df.NewRaceID==i)&(target_df.jockey==target_jockey)].from_odds.values.tolist()[0])

    else:
        target_jockey_odds.append("なし")

# print("target_jockey_odds",target_jockey_odds)
print(len(target_jockey_odds))

#ターゲット騎手の人気リストを作成

for i in NewRaceID_list:
    if i in target_jockey_NewRaceID_list:

        # print("騎手のチェック")
        # print(type(target_df[(target_df.NewRaceID==i)].jockey))
        # print(target_df[(target_df.NewRaceID==i)].jockey)
        # print(target_jockey)

        target_jockey_ninki.append(target_df[(target_df.NewRaceID==i)&(target_df.jockey==target_jockey)].win_ninki.values.tolist()[0])

    else:
        target_jockey_ninki.append("なし")



# print("target_jockey_ninki",target_jockey_ninki)
# print(len(target_jockey_ninki))


# In[41]:


math.ceil(mm/100)*100


# In[42]:


print("スタート")

for i in NewRaceID_list:

    print(i,"レース目")
    print(target_place_ninki_list[i-1])
    print("1着",win_ninki_list[i-1],"番人気")
    print(type(countdown_ninki))

#     print("単勝",target_ninki_odds[i-1],"倍")

    #カウントダウン人気がターゲット着順内に入っていないかの判定
    if not countdown_ninki in target_place_ninki_list[i-1] :


        print(target_place,"着外")
        losing_streak += 1
        print(losing_streak,"連続着外")
        winning_streak = 0

    else:
        print(target_place,"着内")
        winning_streak += 1
        print(winning_streak,"連続",target_place,"着内")
        losing_streak = 0

        print(losing_streak)
        print(onbet)


    #連敗数が初めて基準を満たした場合の処理
   

    if losing_streak == start_bet_ninki and onbet == 0:
        
        print("連敗数が初めて基準を満たした場合の処理")

        print("次レースからベットスタート")

        bet = initial_bet
        
        
        first_bet += 1


        print("次レースベット金額",bet,"円")
        print("ベットリスト",bet_list)
        print("ベット対象レースリスト",race_list_whenbet)

        #ベット中に指定オッズ未満を見送って１着が来た時に連敗数が０になってしまった時に、スキップされないために
        onbet +=1
        
        

        continue


    #対象人気のオッズがターゲットオッズの基準を満たさない時にスキップする処理
    
    print("対象人気オッズ",target_ninki_odds[i-1],"倍")

    if target_ninki_odds[i-1] != 'なし' and target_ninki_odds[i-1] < odds_minimum:
        
        
        print("対象人気の単勝が",odds_minimum,"倍未満のためスキップ")
        

        continue

    if target_ninki_odds[i-1] != 'なし' and target_ninki_odds[i-1] > odds_max:
        print("対象人気の単勝が",odds_max,"倍を超えるためスキップ")

        continue

    # if target_jockey_odds[i-1] ! = 'なし' and target_jockey_odds[i-1] < odds_minimum:
    #     print("対象騎手の単勝が",odds_minimum,"倍未満のためスキップ")

#     if target_jockey_odds[i-1] != 'なし' and target_jockey_odds[i-1] < odds_minimum:
#         print("対象騎手の単勝が",odds_minimum,"倍未満のためスキップ")

#         continue

#     if target_jockey_odds[i-1] != 'なし' and target_jockey_odds[i-1] > odds_max:
#         print("対象人気の単勝が",odds_max,"倍を超えるためスキップ")

#         continue




    #指定連敗数を満たしていない　かつ　ベット中ではない場合、スキップする
    # 指定した単勝がきたかどうか判断し、連勝数または連敗数に加えてスキップする。
    

    if losing_streak < start_bet_ninki and onbet == 0:
        print("対象人気の連敗数が",start_bet_ninki,"連続着外未満のためスキップ")



#         if losing_streak == start_bet_ninki:
#             print("次レースからベットスタート")
            
            

#             bet = initial_bet
#             bet_list.append(bet)
#             race_list_whenbet.append(i+1)

#             print("次レースベット金額",bet,"円")
#             print("ベットリスト",bet_list)
#             print("ベット対象レースリスト",race_list_whenbet)

            #ベット中に指定オッズ未満を見送って１着が来た時に連敗数が０になってしまった時に、スキップされないために
#         onbet +=1

        continue
    
    
    #上記スキップ条件に当てはまらなかった場合、下記コードが実行される
    
    print("ベット")
    
    
    print("連続損失額",total_bet)
    print("単勝オッズ",target_ninki_odds[i-1])
    
    
    if first_bet == 1:
        
        bet = initial_bet
        first_bet = 0
        
        print("initial_betが適用１")
    #　リセットされた後を想定   
    elif bet == initial_bet and onbet >= 1and bet_reset>=1:
        
        bet = initial_bet
        bet_reset = 0
        
        print("initial_betが適用２")
        

    else:
        bet = math.ceil(margin*total_bet/(target_ninki_odds[i-1]-margin)/100)*100
        print("margin計算が適用")
        print(margin,"×","連続ベット合計",total_bet,"÷","(",target_ninki_odds[i-1],"-",margin,")","÷",100,"×",100)

    total_bet += bet

    print("ベット金額",bet)
    print("連続ベット合計",total_bet)

    bet_list.append(bet)
    race_list_whenbet.append(i)

    print(bet_list)

    onbet += 1
    
    
    #指定した人気が１着でない場合


    if win_ninki_list[i-1] != target_ninki:

        print("ハズレ")

        bet_losing_streak += 1
        print(bet_losing_streak,"連続不的中")

        if len(bet_list) <= 1:
            money = budget - bet
        else:
            money = money - bet
        print("ベット合計",sum(bet_list))
        print("払戻合計",sum(revenue_list))
        print("合計利益",sum(revenue_list)-sum(bet_list))

        print("残金",money)
        if money <= 0:
            print("予算オーバー")
            print("合計利益",sum(revenue_list)-sum(bet_list))
            print("ベットリスト",bet_list)
            print("ベット対象レースリスト",race_list_whenbet)
            break
            
            


        # winning_streak = 0

        #連続不的中数に達した時,リセット
        if bet_losing_streak == stopbet_bylost:

            print(type(total_bet))


            print(total_bet,"円損失中")
            print("損切確定！ベット金額を初回額にリセット。")
            print("連敗数もリセット！")

            #total_betと連敗数、連続不的中数の保存
            maxlost_list.append(total_bet)

            list_empty.append(losing_streak)
            bet_losing_streak_list.append(bet_losing_streak)

            total_bet = 0
            losing_streak = 0
            bet_losing_streak = 0
            bet = initial_bet

            onbet = 0


        else:
            print(type(total_bet))
            print(type(bet))
            
            print(total_bet,"円損失中")



            if bet >= stopbet_bymaxbet:
                print("次回ベット金額が上限を越えたので、初回金額に戻します")
                # ここでベット金額を記録すべきか検討

                bet = initial_bet

                print("次レースベット金額",bet,"円")
                
                bet_reset += 1



            if (money - bet)<= 0:
                print("予算オーバー")
                print("合計利益",sum(revenue_list)-sum(bet_list))
                print("ベットリスト",bet_list)
                print("ベット対象レースリスト",race_list_whenbet)
                break

            print("ベット合計",sum(bet_list))
            print("払戻合計",sum(revenue_list))

        




            onbet += 1

    
    #指定した人気が１着の場合
    else:
        print("当たり！")

        if bet_losing_streak >= 1:
            print("連続不的中ストップ")

            
        #ここ重複してないか検討
        
        #連敗数、連続不的中の保存
        bet_losing_streak_list.append(bet_losing_streak)
        list_empty.append(losing_streak)
        maxlost_list.append(total_bet)
        print("連敗数",losing_streak)
        print("ベット連敗数",bet_losing_streak)
        print("的中までの損失累積額",total_bet,"円")


        #配当計算
        revenue_win = win_return_list[i-1]*bet/100
        print("単勝オッズ:",win_return_list[i - 1]/100,"倍","×","ベット金額:",bet,"円")
        print(revenue_win,"円")
        revenue_list.append(revenue_win)
        print("ベットリスト",bet_list)
        print("ベット対象レースリスト",race_list_whenbet)
        print("払戻リスト",revenue_list)

        print("ベット合計",sum(bet_list))
        print("払戻合計",sum(revenue_list))


        total_profit = sum(revenue_list)-sum(bet_list)
        print("合計利益",total_profit)


        if total_profit <= 0:
            print("warning!!!!!!!!!!!!!!!!!!!!!!!!")


        if len(bet_list) == 1:
            money = budget + (revenue_win - bet)
        else:
            money = money + (revenue_win - bet)


        print("残金",money)




        #的中時合計ベット金額の計算
        if i == 1:
            total_bet += initial_bet
        else:
            total_bet += bet

        #的中時利益の計算(re_matingaleの場合はtotal_betではなくbetで計算)
        profit = revenue_win - total_bet

        profit_list.append(profit)
        print("的中時利益:",profit)

        print("合計利益:",total_profit)
        print("上限金額",stop_bymaxprofit)

        if total_profit > stop_bymaxprofit:
            print("合計利益が上限を超えたので、ストップ")
            break

        #次回ベット金額の計算
        bet = initial_bet
        print("次回ベット金額",bet,"円")
        # bet_list.append(bet)
        print("ベットリスト",bet_list)

        print("ベット対象レースリスト",race_list_whenbet)

        #連敗数,連続不的中,total_betの初期化
        losing_streak = 0
        bet_losing_streak = 0
        total_bet = 0

        onbet = 0


mxlost = max(bet_losing_streak_list,default=0)
print("最大不的中数",mxlost)
print(list_empty)
mx = max(list_empty,default=0)
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
print("払戻合計:",sum(revenue_list))
return_sum = sum(revenue_list)

count_bet = len(bet_list)

#利益
profit_result = return_sum - bet_sum

#回収率
if bet_sum != 0 or return_sum != 0:
    recovery_rate = (return_sum/bet_sum)*100
else:
    recovery_rate = 0 

#     #martingale()


# １００円ベットの後に、オッズスキップされた場合に、１００円ベットのまま残る問題を解決したい
# 
