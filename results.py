import sqlite3
import datetime

def connect():
    conn=sqlite3.connect("pollerresults.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pollerresults (id integer PRIMARY KEY, polltime text, location text, dnsserver text, edgeip text, result text,loadtime text,adjloadtime text,coordinates text)")
    conn.commit()
    conn.close()

def add(polltime,location,dnsserver,edgeip,result,loadtime,adjloadtime,coordinates):
    conn=sqlite3.connect("pollerresults.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO pollerresults VALUES(NULL,?,?,?,?,?,?,?,?)",(polltime,location,dnsserver,edgeip,result,loadtime,adjloadtime,coordinates))
    conn.commit()
    conn.close()

def delete(id):
    conn=sqlite3.connect("pollerresults.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM pollerresults WHERE id=?", (id,))
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect("pollerresults.db")
    cur=conn.cursor()
    cur.execute("SELECT * from pollerresults")
    rows=cur.fetchall()
    conn.close()
    return rows

def jsonconverter():
    jsonout = []
    conn=sqlite3.connect("pollerresults.db")
    cur=conn.cursor()
    cur.execute("SELECT * from pollerresults")
    rows=cur.fetchall()
    conn.close()
    for row in rows:
        jsonappend = '{"type": "Feature","geometry": { "type": "Point","coordinates": '+row[8]+'},"properties":{ "Time" :"'+row[1]+'","Location" :'+row[2]+'}},'
        jsonout.append(jsonappend)
    return jsonout

def failedlist():
    jsonout = []; jsonstatus = []
    conn=sqlite3.connect("pollerresults.db")
    cur=conn.cursor()
    cur.execute("SELECT * from pollerresults")
    rows=cur.fetchall()
    conn.close()
    for row in rows:
        match = 0
        if datetime.datetime.strptime(row[1], "%Y-%m-%d-%H.%M.%S") > datetime.datetime.now()-datetime.timedelta(hours=1) and row[5] == "success":
            if len(jsonout) == 0:
                match = 1
                print("Creating new list for "+row[2])
                cur_list = [row[2],1, row[1], row[8]]
                jsonout.append(cur_list)
            else:
                for cur_list in jsonout:
                    if row[2] in cur_list:
                        match = 1
                        print("Matched existing list.  Updating.")
                        cur_list[1] += 1;
                        if datetime.datetime.strptime(cur_list[2], "%Y-%m-%d-%H.%M.%S") < datetime.datetime.strptime(row[1], "%Y-%m-%d-%H.%M.%S"):
                            cur_list[2] = row[1]
                if match == 0:
                    print("Creating new list for "+row[2])
                    cur_list = [row[2],1, row[1], row[8]]
                    jsonout.append(cur_list)
                    print("List of lists is "+str(jsonout))
    for row in jsonout:
        #jsonappend = '{"type": "Feature","geometry": { "type": "Point","coordinates": '+row[3]+'},"properties":{ "Time" :"'+row[2]+'","Location" :'+row[0]+',"Failures" :'+str(row[1])+'}},'
        jsonappend = '{"type": "Feature","properties":{ "Time" :"'+row[2]+'","Location" :'+row[0]+',"Failures" :'+str(row[1])+'},"geometry":{"type": "Point","coordinates": '+row[3]+'}},'
        jsonstatus.append(jsonappend)
    return jsonstatus

connect()
