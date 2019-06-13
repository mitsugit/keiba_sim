# Generated by Django 2.0.2 on 2018-12-23 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keiba', '0006_logic_countdown_select'),
    ]

    operations = [
        migrations.AddField(
            model_name='logic',
            name='avg_interval',
            field=models.FloatField(blank=True, null=True, verbose_name='マージン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='bet_sum',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='count_bet',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='max_interval',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='mx',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='mx_loss',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='mxlost',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='profit',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='profit_sum',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='recovery_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='マージン'),
        ),
        migrations.AddField(
            model_name='logic',
            name='return_sum',
            field=models.IntegerField(blank=True, null=True, verbose_name='人気着外カウントダウン'),
        ),
    ]