
# coding: utf-8

# In[2]:
#check

# 修正マーチン 法
'''
方針: ベット金額がベット時のオッズに依存するため、「次レースのベット金額」は削除。
「ベット時にベット金額」を表示
ベットスタート時は１００円を損失として計算する
'''





def adjust_martin(margin,target_ninki_odds,target_odds,stop_winning,winning_streak,target_list_ninki,nanban,losing_streak,total_bet, bet,list_empty, bet_list,initial_bet,target_list_return,race_count,profit,revenue_win,profit_list,stop_losing,start_bet):

    import numpy as np
    import math

    bet_winning_streak = 0
    bet_winning_streak_list = []
    bet_losing_streak = 0
    bet_losing_streak_list = []

    maxlost_list = []

    revenue_list = []

    onbet = 0

    bet_list.append(initial_bet)

    for i in target_list_ninki:
        race_count += 1
        print(race_count,"レース目")
        print("単勝",target_ninki_odds[race_count-1],"倍")


        # 対象とする単勝オッズが指定オッズより低い場合、スキップする
        # 指定した単勝がきたかどうか判断し、連勝数または連敗数に加えてスキップする。

        if target_ninki_odds[race_count - 1] < target_odds:

            if i != nanban:
                losing_streak += 1
                print(losing_streak,"連敗")
                winning_streak = 0
            else:
                winning_streak += 1
                print(winning_streak,"連勝")

                losing_streak = 0

            print("単勝が",target_odds,"倍未満のためスキップ")

            if losing_streak == start_bet:
                print("次レースからベットスタート")


                bet = initial_bet
                bet_list.append(bet)

                print("次レースベット金額",bet,"円")
                print("ベットリスト",bet_list)

                #ベット中に指定オッズ未満を見送って１着が来た時に連敗数が０になってしまった時に、スキップされないために
                #onbet +=1

            continue

        #指定連敗数を満たしていない　かつ　ベット中ではない場合、スキップする
        # 指定した単勝がきたかどうか判断し、連勝数または連敗数に加えてスキップする。

        if losing_streak < start_bet and onbet == 0:
            print("連敗数が",start_bet,"連敗未満のためスキップ")

            if i != nanban:
                losing_streak += 1
                print(losing_streak,"連敗")
                winning_streak = 0

            else:
                winning_streak += 1
                print(winning_streak,"連勝")
                losing_streak = 0

            if losing_streak == start_bet:
                print("次レースからベットスタート")

                # bet = initial_bet
                # bet_list.append(bet)

                # print("次レースベット金額",bet,"円")
                # print("ベットリスト",bet_list)

                #ベット中に指定オッズ未満を見送って１着が来た時に連敗数が０になってしまった時に、スキップされないために


            continue

        #上記スキップ条件に当てはまらなかった場合、下記コードが実行される

        #指定した人気が１着でない場合
        if i != nanban:
            onbet += 1
            #ベット開始１レース目の場合
            if onbet == 1:
                total_bet = initial_bet

            bet = margin*total_bet/(target_ninki_odds[race_count-1]-margin)
            bet = math.ceil(bet/100)*100
            bet_list.append(bet)
            print("margin:",margin,"×","損失額:",total_bet,"/","(オッズ:",target_ninki_odds[race_count-1],"-","margin:",margin,")")
            print("ベット金額：",bet)
            print("ベットリスト",bet_list)

            print("ハズレ")
            losing_streak += 1

            print(losing_streak,"連敗")
            bet_losing_streak += 1
            print(bet_losing_streak,"連続不的中")

            winning_streak = 0

            onbet += 1

            #連続不的中数に達した時,リセット
            if bet_losing_streak == stop_losing:
                total_bet += bet

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


                total_bet += bet
                print(total_bet,"円損失中")

                #bet = bet*2


                # if target_ninki_odds[race_count] > margin:
                #     print("margin:",margin,"×","損失額:",total_bet,"(オッズ:",target_ninki_odds[race_count],"-","margin:",margin,")"
                #     bet = margin*total_bet/(target_ninki_odds[race_count]-margin)
                #     bet = np.round(bet,-2)
                #
                # #一旦ゼロにしておく
                # else:
                #     bet = 0
                #
                # bet_list.append(bet)
                # print("次レースベット金額",bet,"円")

                onbet += 1

        #指定した人気が１着の場合
        else:
            onbet += 1
            #ベット開始１レース目の場合
            if onbet == 1:
                total_bet = initial_bet


            bet = margin*total_bet/(target_ninki_odds[race_count-1]-margin)
            bet = math.ceil(bet/100)*100
            bet_list.append(bet)
            print("margin:",margin,"×","損失額:",total_bet,"(オッズ:",target_ninki_odds[race_count-1],"-","margin:",margin,")")
            print("ベット金額：",bet)


            print("当たり！")

            if bet_losing_streak >= 1:
                print("連続不的中ストップ")

            #連敗数、連続不的中の保存
            bet_losing_streak_list.append(bet_losing_streak)
            list_empty.append(losing_streak)
            maxlost_list.append(total_bet)
            print("連敗数",losing_streak)
            print("ベット連敗数",bet_losing_streak)
            print("的中までの損失累積額",total_bet,"円")


            #配当計算
            revenue_win = target_list_return[race_count-1]*bet/100
            print("単勝オッズ:",target_list_return[race_count - 1]/100,"倍","×","ベット金額:",bet,"円")
            print(revenue_win,"円")
            revenue_list.append(revenue_win)
            print("払戻リスト",revenue_list)

            #的中時合計ベット金額の計算
            if race_count == 1:
                total_bet += initial_bet
            else:
                total_bet += bet

            #的中時利益の計算(re_matingaleの場合はtotal_betではなくbetで計算)
            profit = revenue_win - total_bet

            profit_list.append(profit)
            print("的中時利益:",profit)

            #次回ベット金額の計算
            # bet = initial_bet
            # print("次回ベット金額",bet,"円")
            # bet_list.append(bet)
            # print("ベットリスト",bet_list)

            #連敗数,連続不的中,total_betの初期化
            losing_streak = 0
            bet_losing_streak = 0
            total_bet = 0

            onbet = 0





    print(list_empty)
    mx = max(list_empty)
    print("最大連敗数",mx)
    print(maxlost_list)
    mx_loss =max(maxlost_list)
    print("最大損失額",mx_loss,"円")

    print("最大損失額",mx_loss,"円")

    print("的中時利益：",profit_list)
    print("的中時利益合計:",sum(profit_list))

    print("ベット金額合計:",sum(bet_list))

    print("払戻合計:",sum(revenue_list))


    return bet_list, revenue_list
    #martingale()


# #
