from turtle import bgcolor
from urllib.request import urlopen
import json
import certifi
from chart_studio import plotly
import plotly.graph_objects as go
from .models import *


#FETCHING THE DATA FROM THE DATABASE FOR PLOTTING THE GRAPH

#FOR TOTAL CASES

#FECTHING THE DATA FROM THE URL
url = "https://api.covid19tracker.in/data/static/data.min.json"
response = urlopen(url,cafile=certifi.where())
data_json = json.loads(response.read())

#STATE URL DATA
state_url=["andaman-and-nicobar-islands","andhra-pradesh","arunachal-pradesh","assam","bihar","chandigarh","chhattisgarh","dadra-and-nagar-haveli","delhi","goa","gujarat","haryana","himachal-pradesh","jammu-and-kashmir","jharkhand","karnataka","kerala","ladakh","lakshadweep","madhya-pradesh","maharashtra","manipur","meghalaya","mizoram","nagaland","odisha","puducherry","punjab","rajasthan","sikkim","tamil-nadu","telangana","tripura","uttar-pradesh","uttarakhand","west-bengal"]

#STATE CODE DICTIONARY
dict1 = {
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

#LISTS FOR STORING THE VARIOUS DATA
state = []
totalCases = []
totalDeaths = []
totalRecover = []
totalTested = []
last24cases = []
last24deaths = []
last24recover = []
last24test= []


#STORING THE DATA IN THE RESPECTIVE LISTS
for a, b in dict1.items():
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


    
#FOR LAST UPDATED DATA    
last_updated = data_json["TT"]["meta"]["last_updated"]
last_date = last_updated[:10]
last_time = last_updated[11:19]



#FECTHING THE DATA FROM THE ANOTEHR URL
url1="https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
response = urlopen(url1,cafile=certifi.where())  
data_json = json.loads(response.read())

#FOR ACTIVE CASES RECORD
ac = data_json['activeCases']
acn = data_json['activeCasesNew']
acn_org = acn
acn = abs(acn)
#FOR RECOVERED  RECORD
rec = data_json['recovered']
recNew = data_json['recoveredNew']

#FOR NEW DECEASED RECORD
dths = data_json['deaths']
dthsNew = data_json['deathsNew']




#FUNCTION FOR DISTRICT WISE CASES
def district_wise(num):
    
    url = "https://api.covid19tracker.in/data/static/data.min.json"
    response = urlopen(url,cafile=certifi.where())
    data_json = json.loads(response.read())

    #FETCHING THE DISTRICTS FOR ALL THE STATES
    districts={}

    for a,b in dict1.items():
        dist=data_json[b]['districts']
        li=[]   
        for j in dist:
            li.append(j)
        
        state_dist={
            a:li
        }
        districts[a]=li
    
    #CODE FOR THE GIVEN STATE 
    code=dict1[num]
    
    #DISTRICTS FOR THE GIVEN STATE    
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
    
    return data,ac,acn,rec,recNew,last_time,last_date

