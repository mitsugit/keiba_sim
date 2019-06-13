def logic(request):
    if(request.method == 'POST'):
        form = LogicForm(request.POST)

        request.session['form_data'] = request.POST
        QueryDict = request.session['form_data'] 


        budget = QueryDict.__getitem__('budget')
    
        fix_or_variable = QueryDict.__getitem__('fix_or_variable')
        if 'fix_bet' in QueryDict.keys():
            fix_bet = QueryDict.__getitem__('fix_bet')
       

        logic_list = Logic.objects
        logiclistform = logiclist()


    else:
        logiclistform = logiclist()
        form = LogicForm
        logic_list = Logic.objects

    params = {
        'logiclistform':logiclistform,
        'form':form,
        'logic_list' : logic_list,
    }


    return render(request, 'keiba/logic.html', params)
