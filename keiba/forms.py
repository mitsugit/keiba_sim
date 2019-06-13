from django import forms

from.models import RaceData ,TargetRaceData,TargetRaceID,RaceSettei,Logic

from django.forms import ModelForm
from django.contrib.auth.models import User


class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['username','email','password']

class LogicTestForm(forms.Form):
    send_message = forms.BooleanField(
    label='実行する',
    required=False,
    )
    

class RaceStteiForm(forms.Form):

    
    

    jockey_list = [[x.jockey, x.jockey] for x in RaceData.objects.all()]
    #リストの中の重複を削除
    jockey_unique = [ ("", '指定なし><')]
    for x in jockey_list:
        if x not in jockey_unique:
            jockey_unique.append(x) 

        



    # 開催日をリスト化
    date_list = [[x.start_date, x.end_date] for x in RaceData.objects.all()]
    # リストの中の重複を削除
    #デフォルト値としてdate_listの１番目を設定
    #date_unique1 = [ (date_list[0][0], '指定なし><')]
    date_unique1 = [ ('2017-01-05 00:00:00', '指定なし><')]
    for x in date_list:
        if x not in date_unique1:
            date_unique1.append(x) 
    
    #デフォルト値としてdate_listの最後を設定
    date_unique2 = [ ('2017-12-28 00:00:00', '指定なし><')]
    for x in date_list:
        if x not in date_unique2:
            date_unique2.append(x) 

    



    #距離のリスト化
    distance_list = [[x.from_distance, x.to_distance] for x in RaceData.objects.all()]
    #昇順に並べ替え
    distance_list = sorted(distance_list)
    #リストの中の重複を削除
    distance_unique1 = [ (100, '指定なし><')]
    for x in distance_list:
        if x not in distance_unique1:
            distance_unique1.append(x) 

    distance_unique2 = [ (5000, '指定なし><')]
    for x in distance_list:
        if x not in distance_unique2:
            distance_unique2.append(x)


##### リスト化


    # jockey_unique = self.jockey_unique
    # date_unique1 = self.date_unique1

    # date_unique2 = self.date_unique2

    # distance_unique1 = self.distance_unique1
    # distance_unique2 = self.distance_unique2







    FOOD_CHOICES = [("中山","中山"),("東京","東京"),("新潟","新潟"),("福島","福島")]

    alllist = [("全て","全て")]

    ninki_list =[("",""),("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),\
                    ("10","10"),("11","11"),("12","12"),("13","13"),("14","14"),("15","15"),("16","16"),("17","17"),("18","18") ]

    racetype_list = [("芝","芝"),("ダ","ダ"),("障","障")]


#####入力フィールドの作成

    # race_place = forms.ChoiceField(
    #     label='開催場',
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=FOOD_CHOICES,
    #     required=True,
    # )

    # race_place = forms.CharField(label='開催場所', required=False)
    all_place = forms.ChoiceField(label='開催日全て', widget=forms.CheckboxSelectMultiple,choices=alllist,required=False)

    race_place = forms.MultipleChoiceField(
    label='開催場所',
    widget=forms.CheckboxSelectMultiple(attrs={"checked":""}),
    choices=FOOD_CHOICES,
    required=True,
    )

    start_date = forms.ChoiceField(label='開催日(始)', choices=date_unique1,required=False)
    end_date = forms.ChoiceField(label='開催日(終)', choices=date_unique2,required=False)

    # howmany_race = forms.IntegerField(label='開催日から何レース分',required=False,min_value=0)
    # race_type =forms.ChoiceField(label='芝かダートか障害か',choices=racetype_list,required=False)
    race_type = forms.MultipleChoiceField(
    label='芝かダートか障害か',
    widget=forms.CheckboxSelectMultiple(attrs={"checked":""}),
    choices=racetype_list,
    required=True,
    )

    from_distance = forms.ChoiceField(label='距離(min）', choices=distance_unique1,required=False)
    to_distance = forms.ChoiceField(label='距離(max）', choices=distance_unique2,required=False)

    number_horse_min = forms.IntegerField(label='出走馬数(min)',required=False,min_value=0,max_value=18,initial=10)
    number_horse_max = forms.IntegerField(label='出走馬数(max)',required=False,min_value=0,max_value=18,initial=18)

    win_ninki = forms.ChoiceField(label='人気馬', choices=ninki_list,required=False,initial=1)
    target_jockey = forms.ChoiceField(label='騎手', choices=jockey_unique,required=False)

    odds_minimum = forms.FloatField(label='オッズ（下限）',required=False,widget=forms.NumberInput(attrs={'step':'0.1'}))
    odds_max = forms.FloatField(label='オッズ（上限）',required=False,widget=forms.NumberInput(attrs={'step':'0.1'}))



class LogicForm(forms.Form):

    #
        #各種リストの作成

    logic_list = [[x.id, x.id] for x in Logic.objects.all()]
    
    # logiclist = forms.ChoiceField(label='ロジックリスト', choices=logic_list,required=False)

    # ninki_or_jockey = [('人気','人気'),('ジョッキー','ジョッキー')]
    


    betway_list = [('マーチンゲール','マーチンゲール '),
            ('利益率確定法','利益率確定法'),
            # ('ダランベール','ダランベール'),
            # ('ピラミッド','ピラミッド'),
            # ('ココモ法','ココモ法'),
            # ('オスカーズグラインド法','オスカーズグラインド法'),
            # ('ウィナーズ投資法（◯回連続連敗でスタート','ウィナーズ投資法（◯回連続連敗でスタート'),
            # ('１２３５法（グッドマン法）','１２３５法（グッドマン法）'),
            # ('31法','31法'),
            # ('ラフィーネ法','ラフィーネ法'),
            # ('モンテカルロ法','モンテカルロ法'),
            # ('進化版・数列投資法','進化版・数列投資法'),
            # ('単位資金配分法','単位資金配分法'),
            # ('前回投資額の〇倍','前回投資額の〇倍'),
            # ('目標純利益確定法','目標純利益確定法'),
            ]


    # fix_or_variable_list = [('fix', '固定'),('variable', '変動')]
    select_or_manual_list = [('select', '選択'),('manual', 'マニュアル')]


    ninki_list =[("",""),("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),\
                 ("10","10"),("11","11"),("12","12"),("13","13"),("14","14"),("15","15"),("16","16"),("17","17"),("18","18") ]

    # jockey_list = [[x.jockey, x.jockey] for x in RaceData.objects.all()]
    #リストの中の重複を削除
    # jockey_unique = [ ("", '指定なし><')]
    # for x in jockey_list:
    #     if x not in jockey_unique:
    #         jockey_unique.append(x) 

        # 開催日をリスト化
    
    # race_list = [[x.id, x.id] for x in TargetRaceID.objects.all()]
    race_list = []
    count = 0
    for x in TargetRaceID.objects.all():
        #仮のレースIDを連番でふって表示し、本物のIDを紐付ける
        count += 1
        race_list.append([x.id,count])
       
    
    target_race = forms.ChoiceField(label='ターゲットレース', choices=race_list,required=False)

    # if logiclist != "":
        
    #     obj =Logic.objects.get(id=logiclist)

    #     budget = obj.budget

    # else:
    #     budget = forms.IntegerField(label='予算',widget=forms.NumberInput(attrs={'step':'100','min':'100'}),required=True,initial=20000)
    
    budget = forms.IntegerField(label='予算',widget=forms.NumberInput(attrs={'step':'100','min':'100'}),required=True,initial=20000)
    initial_bet = forms.IntegerField(label='初回ベット金額',widget=forms.NumberInput(attrs={'step':'100','min':'100'}),required=True,initial=100)
    
   
    
    #ベット方法から選択するか、マニュアルかの選択
    
    # select_or_manual = forms.ChoiceField(label='ベット方法選択かマニュアルか',widget=forms.RadioSelect,choices=select_or_manual_list,required=True,initial='select')
    

    
    bet_way = forms.ChoiceField(label='ベット方法選択',widget=forms.RadioSelect,choices=betway_list,required = False)



    #定額か変動額かの選択
    # fix_or_variable = forms.ChoiceField(label='定額か変動か',widget=forms.RadioSelect(attrs = { 'onclick' : "hihyoji();"}),choices=fix_or_variable_list,required=True,initial='fix')
    # fix_or_variable = forms.ChoiceField(label='定額か変動か',widget=forms.RadioSelect,choices=fix_or_variable_list,required=True,initial='fix')

    


    # fix_bet = forms.IntegerField(label='定額',required=False,widget=forms.NumberInput(attrs={'step':'100','min':'100'}))


    # nanbai = forms.FloatField(label='直近ベットの何倍',required=False,widget=forms.NumberInput(attrs={'step':'0.1'}))

    margin = forms.FloatField(label='マージン(総ベット金額の何倍の利益を得たいか）',required=False,widget=forms.NumberInput(attrs={'step':'0.1'}),initial='1.2')



    # reset_when_hit = forms.BooleanField(label='的中でベット金額リセットするか',required=False,initial='false')
    
    
    
    lost_bet_reset = forms.IntegerField(label='ベット額リセット条件（連続不的中数上限）',required=False,min_value=0)
    #的中ではなく一着であることに注意
    win_bet_reset = forms.IntegerField(label='ベット額連続１着リセット',required=False,min_value=0)
    stopbet_bylost = forms.IntegerField(label='ストップ条件・損失額上限',required=False,min_value=0)
    stopbet_bymaxbet = forms.IntegerField(label='ストップ条件・次回ベット金額上限',required=False,initial=10000)
    # stop_when_hit = forms.BooleanField(label='的中でストップするか',required=False)

    stop_bymaxprofit = forms.IntegerField(label='ストップ条件・合計利益上限',required=False,initial=10000)
    #対象買い目の選択
    # win_bet_select = forms.ChoiceField(label='単勝購入ターゲット',widget=forms.RadioSelect,choices=ninki_or_jockey,required=False,initial="人気")

    target_ninki = forms.ChoiceField(label='人気馬', choices=ninki_list,required=False)
    # target_jockey = forms.ChoiceField(label='騎手', choices=jockey_unique,required=False)

    odds_minimum = forms.FloatField(label='オッズ（下限）',required=False,widget=forms.NumberInput(attrs={'step':'0.1'}))
    odds_max = forms.FloatField(label='オッズ（上限）',required=False,widget=forms.NumberInput(attrs={'step':'0.1'}))

    # countdown_select = forms.ChoiceField(label='カウントダウン対象',widget=forms.RadioSelect,choices=ninki_or_jockey,required=False,initial="人気")

    countdown_ninki = forms.IntegerField(label='カウントダウン対象人気',required=False,min_value=0)
    # countdown_jockey = forms.ChoiceField(label='カウントダウン騎手', choices=jockey_unique,required=False)

    start_bet_ninki = forms.IntegerField(label='着外カウントダウン',required=False,min_value=0,initial=1)
    # start_bet_jockey = forms.IntegerField(label='騎手着外カウントダウン',required=False,min_value=0)
    target_place = forms.IntegerField(label='対象着',required=False,min_value=1,initial=1) 

    
# class RaceRecordForm(forms.Form):
#     send_message = forms.BooleanField(
#     label='登録する',
#     required=False,
#     )

class RaceRecordForm(forms.ModelForm):
    class Meta:
        model = RaceSettei
        fields = ['race_place','start_date','end_date','race_type',\
        'from_distance','to_distance','number_horse_min','number_horse_max',\
        'win_ninki','target_jockey','odds_minimum','odds_max']



class RecordButtonForm(forms.Form):
    send_message = forms.BooleanField(
    label='登録する',
    required=False,
    )


# 保存用モデルフォーム
class LogicRecordForm(forms.ModelForm):
    class Meta:
        model = Logic
        fields = ['target_race','budget','initial_bet','select_or_manual',\
        'bet_way','fix_or_variable','fix_bet','nanbai','reset_when_hit','lost_bet_reset','win_bet_reset','stopbet_bylost',\
        'stopbet_bymaxbet','stop_when_hit','stop_bymaxprofit','countdown_select','target_ninki','target_jockey','odds_minimum','odds_max',\
        'countdown_ninki','countdown_jockey','start_bet_ninki','start_bet_jockey','target_place',\
        'margin','mxlost', 'mx', 'mx_loss', 'profit_sum', 'bet_sum', 'return_sum','count_bet', 'profit', 'recovery_rate',\
        'max_interval', 'avg_interval']


class logiclist(forms.Form):
    logic_list = [[x.id, x.id] for x in Logic.objects.all()]
    
    logiclist = forms.ChoiceField(label='ロジックリスト', choices=logic_list,required=False)


class LogicLoadForm(forms.Form):
    send_message = forms.BooleanField(
    label='読み込む',
    required=False,
    )

