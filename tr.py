from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
import json

# Create your views here.

def cases(request):
    

    url = "https://api.rootnet.in/covid19-in/stats/latest"
    url1="https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"


    #DATA FORM THE FIRST API
    response = urlopen(url)  
    data_json = json.loads(response.read())
    
    state = []
    confirmedIndian = []
    confirmedForiegn = []
    discharged = []
    deaths = []
    totalConfirmed = []

    for x in data_json['data']['regional']:
        state.append(x['loc'])
        confirmedIndian.append(x['confirmedCasesIndian'])
        confirmedForiegn.append(x['confirmedCasesForeign'])
        discharged.append(x['discharged'])
        deaths.append(x['deaths'])
        totalConfirmed.append(x['totalConfirmed'])

    print(confirmedIndian)
    print(confirmedForiegn)
    #DATA FROM THE SECOND API
    response = urlopen(url1)  
    data_json = json.loads(response.read())
    
    activeCases=[]
    newInfected=[]
    recovered=[]    
    newRecovered=[]
    deceased=[]
    newDeceased=[]

    for x in data_json['regionData']:
        activeCases.append(x["activeCases"])
        newInfected.append(x["newInfected"])
        recovered.append(x['recovered'])
        newRecovered.append(x['newRecovered'])
        deceased.append(x['deceased'])
        newDeceased.append(x['newDeceased'])

    ac = data_json['activeCases']
    acn = data_json['activeCasesNew']

    rec = data_json['recovered']
    recNew = data_json['recoveredNew']

    dths = data_json['deaths']
    dthsNew = data_json['deathsNew']
    #PRINTING THE DATA FROM THE FIRST API
    # print(len(state),state)
    # print(len(confirmedIndian),confirmedIndian)
    # print(len(confirmedForiegn),confirmedForiegn)
    # print(len(discharged),discharged)
    # print(len(deaths),deaths)
    # print(len(totalConfirmed),totalConfirmed)

    # # #PRINTING THE DATA FROM THE SECOND API
    # print(activeCases)
    # print(newInfected)
    # print(recovered)
    # print(newRecovered)
    # print(deceased)
    # print(newDeceased)
    data = zip(state,activeCases,newInfected,totalConfirmed,confirmedIndian,confirmedForiegn,recovered,newRecovered,deceased,newDeceased)
    # for a,b,c,d,e,f,g,h,i,j in data:
    #     print(d,"----",e)
    context_dict = {
        'data':data,
        'ac':ac,
        'acn':acn,
        'rec':rec,
        'recNew':recNew,
        'dths':dths,
        'dthsNew':dthsNew
    }

    return render(request,'cases.html',context_dict)
