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
from .fetch_data import *
from .models import India_data
import time
import threading

def update():
    print("Updating--")

def updating_database():
    while True:
        update()
        time.sleep(10)#6HRS


t1 = threading.Thread(target=updating_database)
t1.start()


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
        colorscale='reds',
    

        colorbar=dict(
            title="Cases",

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
        height=650,
        width=550
    )    

    india_map_html = fig.to_html()
    
    return india_map_html


#FUNCTION FOR PLOTTING THE GRAPH
def graph(datax,datay,name,color,title):
    totalcases = go.Figure()
    totalcases.add_trace(go.Scatter(x=datax, y=datay, mode='lines',
            name=name,connectgaps=True,line_color=color,fill='tozeroy'))

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
        
        title=title,
        title_x=0.5,
        title_font_size=23
    )

    return totalcases.to_html()


#FUNCTION FOR PASSING THE DATA TO PLOT GRAPH
def plot_graph():
    #TOTAL CASES GRAPH FOR EVERY TIME DURATION
    alltime=graph(date,Cases,'Total Cases','blue',"Confirmed Cases")
    Tweek=graph(date[-14:],Cases[-14:],'Total Cases','blue',"Confirmed Cases")
    One_month=graph(date[-30:],Cases[-30:],'Total Cases','blue',"Confirmed Cases")
    Three_month=graph(date[-90:],Cases[-90:],'Total Cases','blue',"Confirmed Cases")
    six_month=graph(date[-180:],Cases[-180:],'Total Cases','blue',"Confirmed Cases")

    allTime=[alltime,Tweek,One_month,Three_month,six_month]

    #NO OF DECEASED  GRAPH FOR EVERY TIME DURATION
    alltime=graph(date,deceased,'Total Cases','red',"Deaths")
    Tweek=graph(date[-14:],deceased[-14:],'Total Cases','red',"Deaths")
    One_month=graph(date[-30:],deceased[-30:],'Total Cases','red',"Deaths")
    Three_month=graph(date[-90:],deceased[-90:],'Total Cases','red',"Deaths")
    six_month=graph(date[-180:],deceased[-180:],'Total Cases','red',"Deaths")

    Deceased=[alltime,Tweek,One_month,Three_month,six_month]
    

    #NO OF RECOVERED  GRAPH FOR EVERY TIME DURATION
    alltime=graph(date,recovered,'Total Cases','green',"Recovered")
    Tweek=graph(date[-14:],recovered[-14:],'Total Cases','green',"Recovered")
    One_month=graph(date[-30:],recovered[-30:],'Total Cases','green',"Recovered")
    Three_month=graph(date[-90:],recovered[-90:],'Total Cases','green',"Recovered")
    six_month=graph(date[-180:],recovered[-180:],'Total Cases','green',"Recovered")

    Recovered=[alltime,Tweek,One_month,Three_month,six_month]

    return allTime,Deceased,Recovered



def state_wise(request):
    
    data = zip(state,totalCases,last24cases,totalRecover,last24recover,totalDeaths,last24deaths,totalTested,last24test,state_url)

    Graph=plot_graph()
    Deceased=Graph[1]
    Recovered=Graph[2]
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
        "graph":Graph[0],
        "deceased":Deceased,
        "recovered":Recovered

    }

    return render(request,'cases.html',cont_dict)



#FUNCTION FOR CONVERTING andaman-nicobar into Andaman Nicobar
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
    num=num.replace(" And"," and")
    #FUNCTION FOR GETTING THE DATA FOR THE DSTRICTS OF THE STATE
    data_list=district_wise(num)
    
    data=data_list[0]
    #data,ac,acn,rec,recNew,last_time,last_date
    ac=data_list[1]
    acn=data_list[2]
    rec=data_list[3]
    recNew=data_list[4]
    last_time=data_list[5] 
    last_date=data_list[6]


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



