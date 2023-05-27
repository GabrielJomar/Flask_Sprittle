import mysql.connector


#mycursor.execute("CREATE DATABASE oeelogin")
#mycursor.execute("CREATE TABLE signup (name VARCHAR(255),email VARCHAR(255), password  VARCHAR(255))")

def sqlsignup(nm,emal,pwd):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="12345678",
      database="oeelogin"
    )

    mycursor = mydb.cursor()

    
    sql = "INSERT INTO signup (name,email,password) VALUES (%s,%s, %s)"
    val = (nm,emal,pwd)
    mycursor.execute(sql, val)
    mydb.commit()


def sqllogin(email,password):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="12345678",
      database="oeelogin"
    )

    mycursor = mydb.cursor()

    query = f"SELECT password FROM signup WHERE email='{email}'"
    mycursor.execute(query)
    pas=mycursor.fetchone()
    if not pas:
        return "nouser"
    elif pas[0]==password:
        return "found"
    else:
         return "wrongpass"
    
    
    