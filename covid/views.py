from multiprocessing import context
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
import json
import certifi
from datetime import datetime
import folium
from chart_studio import plotly
import plotly.graph_objects as go
from .test import date,Cases,deceased,recovered

def india_map():
    url = "https://api.covid19tracker.in/data/static/data.min.json"

    response = urlopen(url,cafile=certifi.where())

    data_json = json.loads(response.read())

    d = {
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

    state_india_map = ['Andaman & Nicobar',
        'Andhra Pradesh',
        'Arunachal Pradesh',
        'Assam',
        'Bihar',
        'Chandigarh',
        'Chhattisgarh',
        'Dadra and Nagar Haveli and Daman and Diu',
        'Delhi',
        'Goa',
        'Gujarat',
        'Haryana',
        'Himachal Pradesh',
        'Jammu & Kashmir',
        'Jharkhand',
        'Karnataka',
        'Kerala',
        'Ladakh',
        'Madhya Pradesh',
        'Maharashtra',
        'Manipur',
        'Meghalaya',
        'Mizoram',
        'Nagaland',
        'Odisha',
        'Puducherry',
        'Punjab',
        'Rajasthan',
        'Sikkim',
        'Tamil Nadu',
        'Telangana',
        'Tripura',
        'Uttarakhand',
        'Uttar Pradesh',
        'West Bengal'
    ]
    
    last24cases = []

    for a, b in d.items():
        if(a == "Lakshadweep"):
            continue
        if data_json[b]['delta']['confirmed'] == None:
                last24cases.append(0)
        else:
            last24cases.append(data_json[b]['delta']['confirmed'])

    
    import pandas as pd

    fig = go.Figure(data=go.Choropleth(
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locationmode='geojson-id',
        locations=state_india_map,
        z=last24cases,

        autocolorscale=False,
        colorscale='ice_r',

        colorbar=dict(
            title="Active Cases",

            thickness=15,
            len=0.75,
            
            bgcolor='rgba(255,255,255,0.6)',

            tick0=0,
            dtick=10000,

        )
    ))

    fig.update_geos(
        visible=False,
    #     projection=dict(
    #         type='conic conformal',
    #         parallels=[12.472944444, 35.172805555556],
    #         rotation={'lat': 24, 'lon': 80}
    #     ),
        lonaxis={'range': [68, 98]},
        lataxis={'range': [6, 38]}
    )

    fig.update_layout(
        title=dict(
            text="Past 24 hours COVID-19 Cases ",
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10},
        ),
        title_font_size=23,
        margin={'r': 0, 't': 40, 'l': 0, 'b': 0},
        height=700,
        width=650
    )    

    india_map_html = fig.to_html()
    
    return india_map_html

def graph():
    totalcases = go.Figure()
    totalcases.add_trace(go.Scatter(x=date, y=Cases, mode='lines',
            name='Total Cases',connectgaps=True,line_color='blue',fill='tozeroy'))


    totalcases.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='black',
            linewidth=3,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=True,
            showline=True,
            showticklabels=True,
        ),
        
        autosize=False,
        showlegend=False,
        plot_bgcolor='white',
        
        title="Confirmed Cases",
        title_x=0.5,
        title_font_size=23
    )

    totalcases=totalcases.to_html()

    deceased_graph = go.Figure()
    deceased_graph.add_trace(go.Scatter(x=date, y=deceased, mode='lines',
            name='Total Cases',connectgaps=True,line_color='red',fill='tozeroy'))


    deceased_graph.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='black',
            linewidth=3,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=True,
            showline=True,
            showticklabels=True,
        ),
        autosize=False,
        showlegend=False,
        plot_bgcolor='white',
        title="Deaths",
        title_x=0.5,

        title_font_size=23
    )

    deceased_html=deceased_graph.to_html()


    recovered_graph = go.Figure()
    recovered_graph.add_trace(go.Scatter(x=date, y=recovered, mode='lines',
            name='Total Cases',connectgaps=True,line_color='green',fill='tozeroy'))


    recovered_graph.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='black',
            linewidth=3,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=True,
            showline=True,
            showticklabels=True,
        ),
        autosize=False,
        showlegend=False,
        plot_bgcolor='white',
        title="Recovered",
        title_x=0.5,
        title_font_size=23
    )

    recovered_html=recovered_graph.to_html()
    li=[]
    li.append(totalcases)
    li.append(deceased_html)
    li.append(recovered_html) 
    return li


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

        
    Long = [92.90425735525044,
    79.97385121359896,
    94.6623141206647,
    92.68568626290354,
    85.62534126970718,
    76.75872466,
    82.12782675167301,
    73.09454961,
    77.12804518,
    73.86574064544497,
    72.18750518311046,
    76.49894521749557,
    76.85663275206431,
    75.00794343054076,
    85.87307895838461,
    76.24192278091935,
    77.615112,
    76.22961610979901,
    72.82992744,
    78.11342801165362,
    75.32262083676606,
    93.85297164915906,
    91.23060135619838,
    92.82329684757462,
    94.3705421955022,
    85.00227944796377,
    79.71055402955935,
    75.45751370184799,
    74.83894799328242,
    88.50779711921037,
    78.74296176404843,
    79.208824,
    91.65250205094576,
    80.67263981471628,
    78.88461124441214,
    88.15177427577096]

    lat = [11.8454549271684,
    16.557795934792352,
    27.72904985313979,
    26.33608583083341,
    25.766303272306075,
    30.7426,
    21.55195971255835,
    20.215132170000004,
    28.645944300000007,
    15.394225026558736,
    22.37819881436921,
    29.229507750953644,
    31.65320768629747,
    33.63368522304364,
    23.754476578925654,
    14.3876463059163,
    10.299734542561,
    34.209515,
    10.43639053,
    23.631026937997863,
    19.37025338816622,
    24.718395514498585,
    25.478761503653818,
    23.46017562281006,
    26.10100802473572,
    20.534809345326444,
    11.87026028793732,
    30.923044104266943,
    26.4739224241132,
    27.34002317274592,
    11.128512112685732,
    17.123184,
    23.70753329973328,
    27.05221058971433,
    29.930554662588083,
    23.401895343482565]

    india = folium.Map(location = [20.5937,78.9629],zoom_start=4.5)

    for state,lat,long,conf,Dec,Recov,last24cases in zip(state,lat,Long,totalCases,totalDeaths,totalRecover,last24cases):
                                                
    #for creating circle marker
        folium.CircleMarker(location = [lat,long],
        radius = 5,
        color='red',
        fill = True,
        fill_color='red').add_to(india)    #for creating marker
        folium.Marker(location = [lat,long],popup=folium.Popup(('<strong>State : '+str(state)+'</strong> <br>' +
        '<strong>Confirmed : '+str(conf)+'</strong><br>' +
        '<strong><font color= red>Deceased : </font>'+str(Dec)+'</strong><br>' +
        '<strong><font color=green>Recovered : </font>'+str(Recov)+'</strong><br>' +
        '<strong>Last 24 hours cases : '+str(last24cases)+'</strong><br>' ),max_width=200)).add_to(india)


    map=india._repr_html_()
    
    Graph=graph()
    india_map_graph = india_map()

    cont_dict = {
        'data':data,
        'ac':ac,
        'acn':acn,
        'rec':rec,
        'recNew':recNew,
        'dths':dths,
        'dthsNew':dthsNew,
        "last_date":last_date,
        "last_time":last_time,
        "india_map_graph":india_map_graph,
        "graph":Graph

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



