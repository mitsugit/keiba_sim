from django.contrib import admin

from import_export import resources

from import_export.admin import ImportExportModelAdmin
from import_export import fields
from .models import RaceData,TargetRaceData,TargetRaceID,RaceSettei,Logic
# Register your models here.

class RaceResource(resources.ModelResource):

    class Meta:
        model = RaceData
        widgets = {
                'published': {'format': '%d.%m.%Y'},
                }
        skip_unchanged = True
        report_skipped = False
        #import_id_fields = ('isbn',)
        fields = ('id', 'start_date', 'end_date','race_place','race_number','place_number',\
        'win_ninki','waku_number1','waku_number2','uma_number1','uma_number2',\
        'cource','uma_sex','uma_age','uma_name','from_distance','to_distance',\
        'trainer','jockey','from_odds','to_odds','win_return','race_ID','day_ID','number_horse')

class RaceDataAdmin(ImportExportModelAdmin):
    resource_class = RaceResource


admin.site.register(RaceData, RaceDataAdmin)
admin.site.register(TargetRaceData)
admin.site.register(TargetRaceID)
admin.site.register(RaceSettei)
admin.site.register(Logic)