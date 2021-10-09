from MySQLdb import cursors
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, form, validators
from passlib.hash import sha256_crypt
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("İf you want see this page, you should log in","danger")
            return redirect("login")
    return decorated_function

class RegisterForm(Form):
    name = StringField("name surname", validators=[validators.DataRequired(message="You can not space to name"), validators.Length(
        min=4, max=25, message="please type greater then 3,leaster then 26 character")])
    username = StringField("username", validators=[validators.DataRequired(message="You can not space to name"), validators.Length(
        min=5, max=35, message="please type greater then 4,leaster then 36 character")])
    email = StringField("email", validators=[validators.Email(message="provide a valid email")])
    password= PasswordField("password",validators=[
        validators.DataRequired(message="You can not space to name"),
        validators.EqualTo(fieldname="confirm")
        ])
    confirm=PasswordField("verify password")

class LogInForm(Form):
    username=StringField("USERNAME",validators=[validators.DataRequired(message="please provide your username")])
    password= PasswordField("PASSWORD",validators=[validators.DataRequired("Please provide ypur password")])

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zsaasf'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskproject"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def index():
    number = [1, 2, 3, 4, 5, 6]
    dictList = [
        {"id": 1, "title": "deneme1", "content": "Deneme content 1"},
        {"id": 2, "title": "deneme2", "content": "Deneme content 2"},
        {"id": 3, "title": "deneme3", "content": "Deneme content 3"},
        {"id": 4, "title": "deneme4", "content": "Deneme content 4"}
    ]
    return render_template("index.html", answer="no", numbers=number, dictList=dictList)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles/<string:id>")
def articlesWithId(id):
    return f"Article id is {id}"

@app.route("/register",methods=["GET","POST"])
def reqister():
    form= RegisterForm(request.form)
    if request.method=="POST" and form.validate() :
        name= form.name.data
        username= form.username.data
        email= form.email.data
        password= sha256_crypt.encrypt(form.password.data)
        cursor= mysql.connection.cursor()

        queryString= f"insert into users(name,username,email,password) values( %s,%s,%s,%s )"
        cursor.execute(queryString,(name,username,email,password))
        mysql.connection.commit()
        cursor.close()
        flash("congrats you has been registered","success")
        return redirect(url_for("login"))
    return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form= LogInForm(request.form)
    if request.method=="POST" and form.validate():
        username= form.username.data
        password= form.password.data
        queryString="select * from users where username = %s"
        cursor= mysql.connection.cursor()
        result= cursor.execute(queryString,(username,)) 
        if result>0:
            data= cursor.fetchone()
            realpassword= data["password"]
            if sha256_crypt.verify(password,realpassword):
                flash("you have successfully logged in","success")
                session["logged_in"]=True
                session["user"]=username
                return redirect(url_for("index"))
            else:
                flash("Your entered password is wrong","danger")    
                return redirect(url_for("login"))

        else:
            flash("User has not found. Please check your inputs...","danger")
            return redirect(url_for("login"))
    return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    if not "logged_in" in session:
        flash("you already been logged out","warning")
    else:
        session.clear()
        flash("You have succesfully logged out","danger")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/addarticle",methods=["GET","POST"])
@login_required
def addarticle():
    form=ArticleForm(request.form)
    if request.method=="POST" and form.validate():
        title= form.title.data
        content= form.content.data
        queryString="insert into articles(title,author,content) values(%s,%s,%s)"
        cursor= mysql.connection.cursor()
        cursor.execute(queryString,(title,session["user"],content))
        mysql.connection.commit()
        cursor.close()
        flash("The Article has successfully added","success")
        return redirect(url_for("dashboard"))
    return render_template("addarticle.html",form=form)

#Artcile Form
class ArticleForm(Form):
    title= StringField("ARTICLE HEADER",validators=[validators.Length(min=5,max=100)])
    content= TextAreaField("CONTENT AREA",validators=[validators.Length(min=10)])


@app.route("/articles")
def articles():
    cursor= mysql.connection.cursor()
    result= cursor.execute("select * from articles")
    if result>0:
        articles=cursor.fetchall()
        return render_template("articles.html",articles=articles)
    else:
        return render_template("articles.html")

if __name__ == '__main__':
    app.run(debug=True)


