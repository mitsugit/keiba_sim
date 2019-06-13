from django.db import models


# Create your models here.

class RaceData(models.Model):
    class Meta:
        db_table = 'RaceData'

    # TODO: Define fields here
    # tekito_no = models.IntegerField('適当番号', blank=True, null=True)
    start_date = models.CharField('開催日(始）', blank=True, max_length=100)
    end_date = models.CharField('開催日（終）', blank=True, max_length=100)
    race_place = models.CharField('競馬場', blank=True, max_length=100)
    # race_number = models.IntegerField('番号', blank=True, null=True)
    race_number = models.IntegerField('レース', blank=True, null=True)
    place_number = models.IntegerField('着順', blank=True, null=True)
    win_ninki = models.IntegerField('人気', blank=True, null=True)
    # waku_number = models.IntegerField('枠番', blank=True, null=True)
    # uma_number = models.IntegerField('馬番', blank=True, null=True)
    # 新規追加
    waku_number1 = models.IntegerField('枠番(内）', blank=True, null=True)
    waku_number2 = models.IntegerField('枠番（外）', blank=True, null=True)
    uma_number1 = models.IntegerField('馬番(内）', blank=True, null=True)
    uma_number2 = models.IntegerField('馬番（外）', blank=True, null=True)
    cource = models.CharField('コース', blank=True, max_length=100)
    uma_sex = models.CharField('性別', blank=True, max_length=100)
    uma_age = models.IntegerField('年齢', blank=True, null=True)

    uma_name = models.CharField('馬名', blank=True, max_length=100)
    # 距離は一時的にintegerにはしません。後で、パイソンファイルで加工するコードがあります。
    # この時点で、エクセルファイルを修正すべきか、質問。
    from_distance = models.CharField('距離（上限）', blank=True, max_length=100)
    to_distance = models.CharField('距離（下限）', blank=True, max_length=100)
    trainer = models.CharField('調教師', blank=True, max_length=100)

    jockey = models.CharField('騎手', blank=True, max_length=100)
    from_odds = models.FloatField('単勝（下限）', blank=True, null=True)
    to_odds = models.FloatField('単勝（上限）', blank=True, null=True)
    win_return = models.IntegerField('単勝払戻', blank=True, null=True)
    race_ID = models.IntegerField('race_ID', blank=True, null=True)
    day_ID = models.IntegerField('day_ID', blank=True, null=True)
    number_horse = models.IntegerField('number_horse', blank=True, null=True)


class TargetRaceID(models.Model):
    class Meta:
        db_table = 'TargetRaceID'

    target_RaceID = models.CharField('ターゲットレースID', blank=True, max_length=1000000000000000)


class TargetRaceData(models.Model):
    class Meta:
        db_table = 'TargetRaceData'

    start_date = models.CharField('開催日(始）', blank=True, max_length=100)
    end_date = models.CharField('開催日（終）', blank=True, max_length=100)
    race_place = models.CharField('競馬場', blank=True, max_length=100)
    # race_number = models.IntegerField('番号', blank=True, null=True)
    race_number = models.IntegerField('レース', blank=True, null=True)
    place_number = models.IntegerField('着順', blank=True, null=True)
    win_ninki = models.IntegerField('人気', blank=True, null=True)
    # waku_number = models.IntegerField('枠番', blank=True, null=True)
    # uma_number = models.IntegerField('馬番', blank=True, null=True)
    # 新規追加
    waku_number1 = models.IntegerField('枠番(内）', blank=True, null=True)
    waku_number2 = models.IntegerField('枠番（外）', blank=True, null=True)
    uma_number1 = models.IntegerField('馬番(内）', blank=True, null=True)
    uma_number2 = models.IntegerField('馬番（外）', blank=True, null=True)
    cource = models.CharField('コース', blank=True, max_length=100)
    uma_sex = models.CharField('性別', blank=True, max_length=100)
    uma_age = models.IntegerField('年齢', blank=True, null=True)

    uma_name = models.CharField('馬名', blank=True, max_length=100)
    # 距離は一時的にintegerにはしません。後で、パイソンファイルで加工するコードがあります。
    # この時点で、エクセルファイルを修正すべきか、質問。
    from_distance = models.CharField('距離（上限）', blank=True, max_length=100)
    to_distance = models.CharField('距離（下限）', blank=True, max_length=100)
    trainer = models.CharField('調教師', blank=True, max_length=100)

    jockey = models.CharField('騎手', blank=True, max_length=100)
    from_odds = models.FloatField('単勝（下限）', blank=True, null=True)
    to_odds = models.FloatField('単勝（上限）', blank=True, null=True)
    win_return = models.IntegerField('単勝払戻', blank=True, null=True)
    race_ID = models.IntegerField('race_ID', blank=True, null=True)
    day_ID = models.IntegerField('day_ID', blank=True, null=True)
    number_horse = models.IntegerField('number_horse', blank=True, null=True)


class RaceSettei(models.Model):
    class Meta:
        db_table = 'RaceSettei'

    race_place = models.CharField('競馬場', blank=True, max_length=100)

    start_date = models.CharField('開催日(始）', blank=True, max_length=100)
    end_date = models.CharField('開催日（終）', blank=True, max_length=100)

    race_type = models.CharField('コース', blank=True, max_length=100)

    from_distance = models.CharField('距離（上限）', blank=True, max_length=100)
    to_distance = models.CharField('距離（下限）', blank=True, max_length=100)

    number_horse_min = models.IntegerField('出走馬数(min)', blank=True, null=True)
    number_horse_max = models.IntegerField('出走馬数(max)', blank=True, null=True)

    win_ninki = models.IntegerField('人気', blank=True, null=True)
    target_jockey = models.CharField('騎手', blank=True, max_length=100)

    odds_minimum = models.FloatField('単勝（下限）', blank=True, null=True)
    odds_max = models.FloatField('単勝（上限）', blank=True, null=True)
    howmany_race = models.IntegerField('対象レース数', blank=True, null=True)
    max_interval = models.IntegerField('最大レース間隔数', blank=True, null=True)
    avg_interval = models.IntegerField('平均レース間隔数', blank=True, null=True)


class Logic(models.Model):
    class Meta:
        db_table = 'Logic'

    target_race = models.IntegerField('ターゲットレース', blank=True, null=True)

    budget = models.IntegerField('予算', blank=True, null=True)

    initial_bet = models.IntegerField('初回ベット金額', blank=True, null=True)

    # ベット方法から選択するか、マニュアルかの選択
    select_or_manual = models.CharField('select_or_manual', blank=True, max_length=100)

    bet_way = models.CharField('ベット方法選択', blank=True, max_length=100)

    # 定額か変動額かの選択
    fix_or_variable = models.CharField('固定か変動か', blank=True, max_length=100)
    fix_bet = models.IntegerField('定額', blank=True, null=True)

    nanbai = models.FloatField('直近ベットの何倍', blank=True, null=True)

    reset_when_hit = models.NullBooleanField(null=True)
    lost_bet_reset = models.IntegerField('連続不的中リセット', blank=True, null=True)
    # 的中ではなく一着であることに注意

    win_bet_reset = models.IntegerField('連続１着リセット', blank=True, null=True)
    stopbet_bylost = models.IntegerField('連続不的中上限', blank=True, null=True)
    stopbet_bymaxbet = models.IntegerField('次回ベット金額上限', blank=True, null=True)
    stop_when_hit = models.NullBooleanField(null=True)

    stop_bymaxprofit = models.IntegerField('合計利益上限', blank=True, null=True)

    # 対象買い目の選択
    target_ninki = models.IntegerField('人気', blank=True, null=True)
    target_jockey = models.CharField('騎手', blank=True, max_length=100)

    odds_minimum = models.FloatField('単勝オッズ下限', blank=True, null=True)
    odds_max = models.FloatField('単勝オッズ上限', blank=True, null=True)

    countdown_select = models.CharField('騎手かジョッキーか', blank=True, max_length=100)

    countdown_ninki = models.IntegerField('カウントダウン対象人気', blank=True, null=True)
    countdown_jockey = models.CharField('カウントダウン対象騎手', blank=True, max_length=100)

    start_bet_ninki = models.IntegerField('人気着外カウントダウン', blank=True, null=True)
    start_bet_jockey = models.IntegerField('騎手着外カウントダウン', blank=True, null=True)
    target_place = models.IntegerField('対象着', blank=True, null=True)

    margin = models.FloatField('マージン', blank=True, null=True)

    # 成績登録用

    # data = [mxlost, mx, mx_loss, profit_sum, bet_sum, return_sum, bet_list, count_bet, profit_result, recovery_rate,
    #         race_list_whenbet, max_interval, avg_interval]

    mxlost = models.IntegerField('最大不的中数', blank=True, null=True)
    mx = models.IntegerField('最大連敗数', blank=True, null=True)
    mx_loss = models.IntegerField('最大損失額', blank=True, null=True)
    profit_sum = models.IntegerField('的中時利益合計', blank=True, null=True)
    bet_sum = models.IntegerField('ベット金額合計', blank=True, null=True)
    return_sum = models.IntegerField('払戻合計', blank=True, null=True)
    count_bet = models.IntegerField('ベット回数', blank=True, null=True)
    profit = models.IntegerField('合計利益', blank=True, null=True)
    recovery_rate = models.FloatField('回収率', blank=True, null=True)
    max_interval = models.IntegerField('最大レース間隔', blank=True, null=True)
    avg_interval = models.FloatField('平均レース間隔', blank=True, null=True)
