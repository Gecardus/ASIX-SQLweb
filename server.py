import sqlite3
from flask import Flask, render_template,url_for,redirect,request
import sqlite3
import hashlib
from createdb import cypher_suite
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    conn=sqlite3.connect("store.db")
    cur=conn.cursor()
    SQL=f'SELECT * FROM products'
    prod=cur.execute(SQL).fetchall()
    return render_template("home.html",products=prod)

@app.route("/login",methods=['GET', 'POST'])
def login():
    logged=False 
    if request.method == "POST":
        conn=sqlite3.connect("store.db")
        
        cur=conn.cursor()
        username=request.form.get('username')
        password=request.form.get('password')
        password=hashlib.sha256(bytes(password,'utf-8')).hexdigest()
        # " OR "1"="1
        # " OR "1"="1"; DROP TABLE users;
        SQL=f'SELECT id,username, password FROM users WHERE username="{username}" AND password="{password}"'
        print(SQL)
        try:
            res=cur.execute(SQL).fetchone()
        except Exception as e:
            return render_template("login.html",errors=e)
        if res:
           print("USER", res[0])
           logged=True
        else:
            return render_template("login.html",errors="El usuario no existe o la contraseña no coincide ")
    if logged:
       return redirect('user/'+str(res[0]))
    else:
        return render_template("login.html")
    
@app.route("/register",methods=['GET','POST'])
def register():
    registered=False
    if request.method == "POST":
        conn=sqlite3.connect("store.db")
        cur=conn.cursor()
        print(request.form)
        ID=str(uuid.uuid4())
        SQL='INSERT INTO users VALUES ('

        SQL+='"'+ID+'",'
        for field in list(request.form):
            campo=field
            valor=request.form[field]
            if campo=='password':
                valor=hashlib.sha256(bytes(valor,'utf-8')).hexdigest()
            
            elif campo=="adress":
                valor=cypher_suite.encrypt(bytes(valor,'utf-8')).decode()
            SQL+=f'"{valor}", '
        SQL=SQL.rstrip(', ')
        SQL+=',"'+str(2)+'"'
        SQL+=')'
        print("create user",SQL)
        try:
            cur.execute(SQL)
            conn.commit()
            newuserid=ID
            registered=True
        except Exception as e:
            return render_template("register.html",errors=e)
    
    if registered:
        return redirect('user/'+str(newuserid))
    else:
        return render_template("register.html")

@app.route("/user/<string:userid>")
def user(userid):
    # get user data
    conn=sqlite3.connect("store.db")
    cur=conn.cursor()
    SQL=f'SELECT username, adress FROM users WHERE id="{userid}"'
    userdata=cur.execute(SQL).fetchone()
    
    #get products
    SQL=f'SELECT name,price,image FROM purchases INNER JOIN products ON purchases.product_id=products.rowid WHERE purchases.username_id="{userid}"'
    prod=cur.execute(SQL).fetchall()
    print("products",prod)
    return render_template("user.html", userdata={"username":userdata[0],"adress":cypher_suite.decrypt(userdata[1]).decode(),"products":prod})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
