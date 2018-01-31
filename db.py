import sqlite3

def connect():
    conn=sqlite3.connect("locations.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS locations (id integer PRIMARY KEY, coordinates text, location text, dnsserver text, user text)")
    conn.commit()
    conn.close()

def add(coordinates,location,dnsserver,user):
    locations = []
    conn=sqlite3.connect("locations.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO locations VALUES(NULL,?,?,?,?)",(coordinates,location,dnsserver,user))
    conn.commit()
    cur.execute("SELECT * from locations")
    rows=cur.fetchall()
    conn.close()
    for row in rows:
        locationsappend = '{"type": "Feature","geometry": { "type": "Point","coordinates": '+row[1]+'},"properties":{ "User" :"'+row[4]+'","Location" :'+row[2]+'}},'
        locations.append(locationsappend)
    monitorsout = open('templates/monitorsout.json','w')
    for line in locations:
        monitorsout.write("%s" % line)
    monitorsout.close()
    with open('templates/monitorsout.json','r+') as f:
        s = f.read(); s = s[:-1]; f.seek(0); f.write('eqfeed_callback({"type":"FeatureCollection","features":[' + s)
    with open('templates/monitorsout.json','a') as f:
        f.write("]});")

def delete(id):
    conn=sqlite3.connect("locations.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM locations WHERE id=?", (id,))
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect("locations.db")
    cur=conn.cursor()
    cur.execute("SELECT * from locations")
    rows=cur.fetchall()
    conn.close()
    return rows

connect()
