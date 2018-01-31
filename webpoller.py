import requests
import dns.resolver
import db
import results
import time
import datetime
import socket
import latency
from operator import itemgetter
from itertools import groupby
import deets

def webpoller():
    # Grab all the Monitor Entries in the database
    rows = db.view()
    for row in rows:
        # For each entry, resolve the hostname of the DNS server if applicable.
        # Create Flag in the event of a DNS issue
        dnserror = 0
        # Timestamp of test
        polltime = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        # Grab the coordinates
        coordinates = row[1]
        # Grab the friendly name of the Location we are testing
        location = row[2]
        myResolver = dns.resolver.Resolver()
        myResolver.timeout = 5
        myResolver.lifetime = 5
        try:
            # Is IP?
            socket.inet_aton(row[3])
            # Then set our DNS server to the IP
            myResolver.nameservers = [row[3]]
        except socket.error:
            # Is not IP?  Then resolve the hostname
            dnsquery = myResolver.query(row[3], "A")
                # We only want the 1st A record
                #myResolver.nameservers = [arecord]
            arecord = dnsquery[0]
            myResolver.nameservers = [arecord]
        dnsserver=myResolver.nameservers[0]
        try:
            # Resove the FQDN we are testing
            cdnip = myResolver.query('www.cbtnuggets.com', "A")
            edgeip = str(cdnip[0])
            # Send HTTP request to edge IP - ignoring SSL errors and sending the correct host header
            r=requests.head('https://'+str(edgeip)+'/health.html',headers={'host': monitoredsite}, verify=False, timeout=5)
        except:
            # IF failure - raise DNS flag
            dnserror = 1
        if dnserror != 1:
            if r.status_code == 200:
                # Get total time taken for requests
                loadtime=r.elapsed.total_seconds()
                # Adjust latency based on latency.py script
                adjlatency=latency.ping_time(edgeip)
                if adjlatency != "latency test failed":
                    adjloadtime=(float(loadtime)-float(adjlatency))
                else:
                    adjloadtime="latency test failed"
                result="success"
                results.add(polltime,location,dnsserver,str(edgeip),result,loadtime,adjloadtime,coordinates)
            else:
                result="failure"
                loadtime="N/A"
                adjloadtime="N/A"
                results.add(polltime,location,dnsserver,str(edgeip),result,loadtime,adjloadtime,coordinates)
        else:
            edgeip="N/A"
            result="DNS Error"
            loadtime="N/A"
            adjloadtime="N/A"
            results.add(polltime,location,dnsserver,str(edgeip),result,loadtime,adjloadtime,coordinates)
    time.sleep(30)
    # Database cleanup ; create json file
    rows = results.view()
    for row in rows:
        if datetime.datetime.strptime(row[1], "%Y-%m-%d-%H.%M.%S") < datetime.datetime.now()-datetime.timedelta(days=14):
            todelete = row[0]
            results.delete(todelete)

    jsonoutredux = results.failedlist()
    jsondocredux = open('templates/jsonout.json','w')
    for line in jsonoutredux:
        jsondocredux.write("%s" % line)
    jsondocredux.close()
    with open('templates/jsonout.json', 'r+') as f:
        s = f.read(); s = s[:-1]; f.seek(0); f.write('eqfeed_callback({"type":"FeatureCollection","features":[' + s)
    with open('templates/jsonout.json', 'a') as f:
        f.write("]});")

while True:
    webpoller()
