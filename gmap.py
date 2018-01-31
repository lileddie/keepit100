import requests
import json
import deets

def translate(city,state,country):
    url="https://maps.googleapis.com/maps/api/geocode/json?address="+str(city)+",+"+str(state)+",+"+str(country)+"&key="+apikey
    response=requests.get(url, timeout=5)
    r = json.dumps(response.json())
    loaded_r = json.loads(r)
    lat=loaded_r["results"][0]["geometry"]["location"]["lat"]
    lon=loaded_r["results"][0]["geometry"]["location"]["lng"]
    return "["+str(lon)+","+str(lat)+"]"
