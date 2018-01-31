from flask import Flask, render_template, request
import db
import results
import gmap
import sqlite3
import monitorverify as mv

app=Flask(__name__)

@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/addmonitor", methods=['GET'])
def addmonitor():
    return render_template("addmonitor.html")

@app.route("/delmonitor", methods=['GET', 'POST'])
def delmonitor():
    if request.method=='GET':
        con = sqlite3.connect("locations.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from locations")
        rows=cur.fetchall()
        return render_template("delmonitor.html", rows = rows)
    if request.method=='POST':
        delete=request.form["Entry"]
        print(delete)
        db.delete(delete)
        con = sqlite3.connect("locations.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from locations")
        rows=cur.fetchall()
        return render_template("delmonitor.html", rows = rows)

@app.route("/addstatus", methods=['POST'])
def addstatus():
    if request.method=='POST':
        user="troy"
        city=request.form["city"]
        state=request.form["state"]
        country=request.form["country"]
        dnsserver=request.form["dnsserver"]
        #user=request.headers.get('REMOTE_USER')
        #place the new monitored region in the DB
        coordinates=gmap.translate(city,state,country)
        location=('"'+city+","+state+","+country+'"')
        results = mv.verify(dnsserver)
        if results == "Failure":
            return render_template("adderror.html")
        db.add(coordinates,location,dnsserver,user)
        return render_template("addstatus.html",location=location)

@app.route("/view", methods=['GET'])
def view():
    con = sqlite3.connect("locations.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from locations")
    rows=cur.fetchall()
    return render_template("view.html",rows = rows)


@app.route("/delstatus", methods=['POST'])
def delstatus():
    if request.method=='POST':
        entry=request.form[entry]
        #Get the active directory username
        user=request.headers.get('REMOTE_USER')
        #place the new monitored region in the DB
        result=db.remove(entry)
        return render_template("delstatus.html",result=result)

@app.route("/details", methods=['GET'])
def details():
    con = sqlite3.connect("pollerresults.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from (SELECT * from pollerresults order by id ASC limit -20) order by id DESC limit 20")
    #cur.execute("SELECT * from pollerresults")
    rows=cur.fetchall()
    con.close()
    return render_template("details.html",rows = rows)

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/jsonout", methods=['GET'])
def jsonout():
    return render_template("jsonout.json")

@app.route("/monitorjsonout", methods=['GET'])
def monitorjsonout():
    return render_template("monitorsout.json")

@app.route("/adderror", methods=['GET'])
def adderror():
    return render_template("adderror.html")


if __name__ == '__main__':
    app.debug=True
    app.run()
