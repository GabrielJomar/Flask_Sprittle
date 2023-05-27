import mysql.connector


#mycursor.execute("CREATE DATABASE video")
#mycursor.execute("CREATE TABLE signup (name VARCHAR(255),email VARCHAR(255), password  VARCHAR(255))")

def sqlsignup(nm,emal,pwd):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="12345678",
      database="video"
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
      database="video"
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    
    mycursor.execute("Select email from signup;")
    users=mycursor.fetchone()
    print(users)
    for i in users:
        print(i,email)
        if email==i:
            print("I found it")

  
            query = f"SELECT password FROM signup WHERE email='{email}'"
            mycursor.execute(query)
            pas=mycursor.fetchall()
            print(pas)
            if pas==password:
                pass
            else:
                print("Incorrect password")
        else:
            print("Invalid user")
    
    '''
    

