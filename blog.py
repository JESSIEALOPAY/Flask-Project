from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


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
def articles(id):
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
        return redirect(url_for("index"))
    else:
        flash("Please check your inputs","danger")
        return render_template("register.html",form=form)

if __name__ == '__main__':
    app.run(debug=True)


