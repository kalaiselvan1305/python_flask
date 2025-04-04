from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)
# MYSQL CONNECTION
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="flask"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

# Loading Home Page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    
    return render_template("home.html", datas=res)

# New User
@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into users(name,age,city) value (%s, %s, %s)" 
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash('User Details Added')
        return redirect(url_for("home"))
    return render_template("addUsers.html")

# Update User
@app.route("/editUser/<string:id>",methods=['GET','POST'])
def editUser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update users set name=%s, age=%s, city=%s where id=%s"
        con.execute(sql, [name,age,city,id])
        mysql.connection.commit()
        con.close()
        flash('User Details Updated')
        return redirect(url_for("home"))
        con=mysql.connection.cursor()

    sql="SELECT * FROM users where id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editUser.html", datas=res)

# Delete User
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from users where id=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted')
    return redirect(url_for("home"))


if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True) 