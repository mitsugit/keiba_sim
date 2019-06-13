    logic_list = [[x.id, x.id] for x in Logic.objects.all()]
    
    logiclist = forms.ChoiceField(label='ロジックリスト', choices=logic_list,required=False)

    obj =Logic.objects.get(id=logiclist)