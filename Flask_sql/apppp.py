from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sql_sql_it import sqlsignup  
from sql_sql_it import sqllogin


app= Flask(__name__)


@app.route("/")
def main():
    return render_template("userlogin.html")



@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       email = request.form.get("email")
       # getting input with name = lname in HTML form
       password = request.form.get("password")
       print(email,password)
       if sqllogin(email,password)=='found':
          # return render_template('oeeout.html')
           return redirect(url_for("oeedata"))
       elif sqllogin(email,password)=='nouser':
           return redirect(url_for("invaliduser"))         
       elif sqllogin(email,password)=='wrongpass':
           return redirect(url_for("incorrect"))
       
        
       
@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       username = request.form.get("username")
       email = request.form.get("email")
       # getting input with name = lname in HTML form
       password = request.form.get("password")
       print(username,email,password)
       sqlsignup(username,email,password)
           #return redirect(url_for("model"))
       return redirect(url_for("main"))
   
@app.route("/invalid",methods=['GET'])
def invaliduser():
    return "<h1>User doesnt exist.</h1>" 


@app.route("/incorrect",methods=['GET'])
def invalid():
    return "<h1>Incorrect Password.</h1>"  
       
        
       
# Route to display the data from the database
@app.route('/', methods=['GET'])
def display_data():
    conn = sqlite3.connect('Data.db')
    cursor = conn.cursor()
    cursor.execute('Select * from dashboard_process')
    global data 
    data = cursor.fetchall()
   # print(data)
    cursor.execute('Select unique_id from dashboard_process')
    u_id = cursor.fetchall()
    #print(u_id)
    
    uid=[]
    for i in u_id:
        if i not in uid:
            uid.append(i)
    #print(uid)
    cursor.execute('Select count (*)from dashboard_process group by unique_id')
    count=cursor.fetchall()
    conn.close()
    time=[]
    cam=[]
    for i in data:
        time.append(float(i[8]))
    for i in data:
        cam.append(i[4])
    #print(time)
    from collections import defaultdict
    list_of_tuples = list(zip(u_id,time))    
    output = defaultdict(list)
    for k,v in list_of_tuples:
        output[k].append(v)
   # print(output)
    
    out = {k: [sum(output[k])] for k in output.keys()}
   # print(out)
    
    
    ict=600
    ao=(len(uid))
    avail=1
    quality=1
    for key in out:
        #print(out[key])
        P=((ict*ao)/out[key][0])*100
        P=P/100
        #print(P)
   # print(out[k][0])  
    perf={k:P for k in out.keys()}
   # print(perf)

    for key in perf:
        #print(perf[key])
        oee=avail*quality*perf[key]*100
        global OEE
    OEE=([(k,oee,cam[0]) for k in out])
    #print(OEE)
    
    
#display_data()    
       
        
    # print(count)
    #return render_template('indexsql.html', data=data)
display_data()


@app.route('/oeedatas', methods=['GET'])
def oeedata():
    return render_template('oeeout.html', OEE=OEE)

@app.route('/settings', methods=['POST'])
def save_settings():
    camera_name = request.form['camera_name']
    oee_threshold = request.form['oee_threshold']
    oee_threshold=float(oee_threshold)
    print(oee_threshold)
    oeefinal=[]
    for i in OEE:
        if (i[1]>oee_threshold and i[2]==camera_name):
            oeefinal.append(i)
    oeefinalout=[]
    for i in data:
        if i[4]==camera_name:
            oeefinalout.append(i)
    print(oeefinalout)
    return render_template('oeefinalout.html', oeefinalout=oeefinalout)

    
if __name__=='__main__':
    app.run(port="5000",host="localhost")


