from multiprocessing import context
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
import json
import certifi
from datetime import datetime




def state_wise(request):

    url = "https://api.covid19tracker.in/data/static/data.min.json"

    response = urlopen(url,cafile=certifi.where())

    data_json = json.loads(response.read())
    state_url=["andaman-and-nicobar-islands","andhra-pradesh","arunachal-pradesh","assam","bihar","chandigarh","chhattisgarh","dadra-and-nagar-haveli","delhi","goa","gujarat","haryana","himachal-pradesh","jammu-and-kashmir","jharkhand","karnataka","kerala","ladakh","lakshadweep","madhya-pradesh","maharashtra","manipur","meghalaya","mizoram","nagaland","odisha","puducherry","punjab","rajasthan","sikkim","tamil-nadu","telangana","tripura","uttar-pradesh","uttarakhand","west-bengal"]

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

        if data_json[b]['delta']['confirmed'] == None:
            last24cases.append('-')
        else:
            last24cases.append(data_json[b]['delta']['confirmed'])

        if data_json[b]['delta']['deceased'] == None:
            last24deaths.append('-')
        else:
            last24deaths.append(data_json[b]['delta']['deceased'])

        if data_json[b]['delta']['recovered'] == None:
            last24recover.append('-')
        else:
            last24recover.append(data_json[b]['delta']['recovered'])

        if data_json[b]['delta']['tested'] == None:
            last24test.append('-')
        else:
            last24test.append(data_json[b]['delta']['tested'])

        if data_json[b]['total']['confirmed'] == None:
            totalCases.append('-')
        else:
            totalCases.append(data_json[b]['total']['confirmed'])

        if data_json[b]['total']['deceased'] == None:
            totalDeaths.append('-')
        else:
            totalDeaths.append(data_json[b]['total']['deceased'])

        
        if data_json[b]['total']['recovered'] == None:
            totalRecover.append('-')
        else:
            totalRecover.append(data_json[b]['total']['recovered'])

        if data_json[b]['total']['tested'] == None:
            totalTested.append('-')
        else:
            totalTested.append(data_json[b]['total']['tested'])


        
        
    last_updated = data_json["TT"]["meta"]["last_updated"]
    last_date = last_updated[:10]
    last_time = last_updated[11:19]
    
    
    # print(data_json[b]['total'])

    # for a, b in dict.items():
    #     state.append(a)
        # if data_json[b]['delta']['confirmed'] == None:
        #     last24cases.append('-')
        # else:
        #     last24cases.append(data_json[b]['delta']['confirmed'])
        
        # if data_json[b]['delta']['tested'] == None:
        #     last24test.append('-')
        # else:
        #     last24test.append(data_json[b]['delta']['tested'])
        
        # if data_json[b]['total']['tested'] == None:
        #     totalTested.append('-')
        # else:
        #     totalTested.append(data_json[b]['total']['tested'])
        
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
    data = zip(state,totalCases,last24cases,totalRecover,last24recover,totalDeaths,last24deaths,totalTested,last24test,state_url)

    cont_dict = {
        'data':data,
        'ac':ac,
        'acn':acn,
        'rec':rec,
        'recNew':recNew,
        'dths':dths,
        'dthsNew':dthsNew,
        "last_date":last_date,
        "last_time":last_time
    }

    return render(request,'cases.html',cont_dict)



def Converter(str):
    str1=str[0].capitalize()
    for i in range(1,len(str)):
        if str[i-1]=='-':
            str1+=str[i].capitalize()
        else:
            if str[i]=='-':
              str1+=' '         
            else:
              str1+=str[i]    
    
    return str1 

def state_wise1(request,num):
    
    num=Converter(num)
    url = "https://api.covid19tracker.in/data/static/data.min.json"

    response = urlopen(url,cafile=certifi.where())

    data_json = json.loads(response.read())

    dict = {
        "Andaman And Nicobar Islands": "AN",
        "Andhra Pradesh": "AP",
        "Arunachal Pradesh": "AR",
        "Assam": "AS",
        "Bihar": "BR",
        "Chandigarh": "CH",
        "Chhattisgarh": "CT",
        "Dadra And Nagar Haveli": "DN",
        "Delhi": "DL",
        "Goa": "GA",
        "Gujarat": "GJ",
        "Haryana": "HR",
        "Himachal Pradesh": "HP",
        "Jammu And Kashmir": "JK",
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

    #THIS IS AN DICTIONARY THAT STORES THE STATE NAME AND LIST OF STATE DISTRICTS 
    districts={}

    for i in dict:
        dist=data_json[dict[i]]['districts']
        li=[]   
        for j in dist:
            li.append(j)
        
        state_dist={
                i:li
        }
        districts[i]=li
    
    code=dict[num]
    state_districts=districts[num]

    districts_new_data=[]
    districts_total_data=[]

    for i in state_districts:
        #FOR THE APST 24 HRS DATA
        temp=[]
        temp.append(data_json[code]['districts'][i]['delta']['confirmed'])
        temp.append(data_json[code]['districts'][i]['delta']['deceased'])
        temp.append(data_json[code]['districts'][i]['delta']['recovered'])
        temp.append(data_json[code]['districts'][i]['delta']['tested'])
        districts_new_data.append(temp)

        #FOR THE TOTAL DATA
        temp=[]
        temp.append(data_json[code]['districts'][i]['total']['confirmed'])
        temp.append(data_json[code]['districts'][i]['total']['deceased'])
        temp.append(data_json[code]['districts'][i]['total']['recovered'])
        temp.append(data_json[code]['districts'][i]['total']['tested'])
        districts_total_data.append(temp)

    data=zip(state_districts,districts_total_data,districts_new_data)

    #FOR OVERALL DATA OF THE STATE
    ac = data_json[code]['total']['confirmed']
    acn = data_json[code]['delta']['confirmed']

    rec = data_json[code]['total']['recovered']
    recNew = data_json[code]['delta']['recovered']

    dths = data_json[code]['total']['deceased']
    dthsNew = data_json[code]['delta']['deceased']

    
    last_updated = data_json[code]["meta"]["last_updated"]
    last_date = last_updated[:10]
    last_time = last_updated[11:19]

    context={
        'data':data,
        'ac':ac,
        'acn':acn,
        'rec':rec,
        'recNew':recNew,
        'dths':dths,
        'dthsNew':dthsNew,
        'last_date':last_date,
        'last_time':last_time
    }

    return render(request,'district_cases.html',context)



