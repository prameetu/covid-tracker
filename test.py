import json
from urllib.request import urlopen
import certifi
import folium

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

state = []
totalCases = []
totalDeaths = []
totalRecover = []
last24cases = []

for a,b in d.items():
        state.append(a)
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
        
        if data_json[b]['delta']['confirmed'] == None:
            last24cases.append('-')
        else:
            last24cases.append(data_json[b]['delta']['confirmed'])

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
 77.615112,
 76.24192278091935,
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
 34.209515,
 10.299734542561,
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


# for i in range(0,len(state)):
#         print(state[i]," ",lat[i]," ",Long[i])

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
    '<strong>Death Rate : '+str(last24cases)+'</strong><br>' ),max_width=200)).add_to(india)

india.save("map.html")
# #FOR SAVING THE IMAGES
# from htmlwebshot import WebShot
# shot = WebShot()
# shot.quality = 100

# image = shot.create_pic(html="/map.html")
