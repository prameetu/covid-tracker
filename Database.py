import imp
from urllib.request import urlopen
import json
import certifi
from chart_studio import plotly
import plotly.graph_objects as go
from .covid.models import India_data



''''
if isupdate true:
    len database != len compute
      update
      to_update false

scheduler 12pm ko to_update true

Update

'''