from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
import json
import certifi



def state_wise(request):

    url = "https://api.covid19tracker.in/data/static/data.min.json"

    response = urlopen(url,cafile=certifi.where())

    data_json = json.loads(response.read())

    dict = {
        "Andaman and Nicobar Islands": "AN",
        "Andhra Pradesh": "AP",
        "Arunachal Pradesh": "AR",
        "Assam": "AS",
        "Bihar": "BR",
        "Chandigarh": "CH",
        "Chhattisgarh": "CT",
        "Dadra and Nagar Haveli": "DN",
        "Delhi": "DL",
        "Goa": "GA",
        "Gujarat": "GJ",
        "Haryana": "HR",
        "Himachal Pradesh": "HP",
        "Jammu and Kashmir": "JK",
        "Jharkhand": "JH",
        "Karnataka": "KA",
        "Kerala": "KL",
        "Ladakh": "LA",
        "Lakshadweep": "LD",
        "Madhya Pradesh": "MP",
        "Maharashtra": "MH",
        "Manipur": "MN",
        "Meghalaya": "ML",
        "Mizoram": "MZ",
        "Nagaland": "NL",
        "Odisha": "OR",
        "Puducherry": "PY",
        "Punjab": "PB",
        "Rajasthan": "RJ",
        "Sikkim": "SK",
        "Tamil Nadu": "TN",
        "Telangana": "TG",
        "Tripura": "TR",
        "Uttar Pradesh": "UP",
        "Uttarakhand": "UT",
        "West Bengal": "WB",
    }

    state = []
    totalCases = []
    totalDeaths = []
    totalRecover = []
    totalTested = []
    last24cases = []
    last24deaths = []
    last24recover = []
    last24test= []

    for a, b in dict.items():
        state.append(a)
        last24cases.append(data_json[b]['delta']['confirmed'])
        last24deaths.append(data_json[b]['delta']['deceased'])
        last24recover.append(data_json[b]['delta']['recovered'])
        last24test.append(data_json[b]['delta']['tested'])
        totalCases.append(data_json[b]['delta']['confirmed'])
        totalDeaths.append(data_json[b]['total']['deceased'])
        totalRecover.append(data_json[b]['total']['recovered'])
        totalTested.append(data_json[b]['total']['tested'])
    
        


    # print(data_json[b]['total'])

    # for a, b in dict.items():
    #     state.append(a)
    #     if data_json[b]['delta']['confirmed'] == None:
    #         last24cases.append('-')
    #     else:
    #         last24cases.append(data_json[b]['delta']['confirmed'])
        
    #     if data_json[b]['delta']['tested'] == None:
    #         last24test.append('-')
    #     else:
    #         last24test.append(data_json[b]['delta']['tested'])
        
    #     if data_json[b]['total']['tested'] == None:
    #         totalTested.append('-')
    #     else:
    #         totalTested.append(data_json[b]['total']['tested'])
        
    #     # last24deaths.append(data_json[b]['delta']['deceased'])
    #     # last24recover.append(data_json[b]['delta']['recovered'])
    #     # totalCases.append(data_json[b]['delta']['confirmed'])
    #     # totalDeaths.append(data_json[b]['total']['deceased'])
    #     # totalRecover.append(data_json[b]['total']['recovered'])
    
    
    url1="https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
    response = urlopen(url1,cafile=certifi.where())  
    data_json = json.loads(response.read())
    
    # for x in data_json['regionData']:
    #     last24deaths.append(x['newDeceased'])
    #     last24recover.append(x['newRecovered'])
    #     totalCases.append(x['totalInfected'])
    #     totalDeaths.append(x['deceased'])
    #     totalRecover.append(x['recovered'])

    ac = data_json['activeCases']
    acn = data_json['activeCasesNew']

    rec = data_json['recovered']
    recNew = data_json['recoveredNew']

    dths = data_json['deaths']
    dthsNew = data_json['deathsNew']
    data = zip(state,totalCases,last24cases,totalRecover,last24recover,totalDeaths,last24deaths,totalTested,last24test)

    cont_dict = {
        'data':data,
        'ac':ac,
        'acn':acn,
        'rec':rec,
        'recNew':recNew,
        'dths':dths,
        'dthsNew':dthsNew
    }

    return render(request,'cases.html',cont_dict)