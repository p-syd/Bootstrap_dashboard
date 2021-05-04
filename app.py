from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from passlib.hash import sha256_crypt

engine = create_engine("sqlite:///test.db")
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
app.config.update({
    'SQLALCHEMY_POOL_SIZE': None,
    'SQLALCHEMY_POOL_TIMEOUT': None
})

app.config['SECRET_KEY'] = 'thisisasecret'

#register
@app.route('/page-register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        securepass = sha256_crypt.encrypt(str(password))

        if name =='' or email == '' or password == '' or cpassword == '':
            flash("You left some fields empty!", "danger")
        else:
            if password == cpassword:
                db.execute("INSERT into REGISTER(username, email, password) VALUES(:name, :email, :password)", {"name":name, "email":email, "password":securepass})
                db.commit()
                flash("Account created!", "success")
                return render_template('page-login.html')
            else:
                flash("password doesn't match", "danger")
                return render_template("page-register.html")
    return render_template('page-register.html')

#login
@app.route('/', methods=["GET", "POST"])
@app.route('/page-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT email FROM REGISTER WHERE email=:email", {"email":email}).fetchone()
        passwordata = db.execute("SELECT password FROM REGISTER WHERE email=:email", {"email":email}).fetchone()

        if usernamedata is None:
            flash("No user found!", "danger")
            return render_template("page-login.html")
        else:
            for pass_data in passwordata:
                if sha256_crypt.verify(password, pass_data):
                    flash("Login successful!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Incorrect Password", "danger")
                    return render_template("page-login.html")
    return render_template('page-login.html')

@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/page-forgot-password', methods=["GET", "POST"])
def recovery():
    if request.method == "POST":
        email = request.form.get("email")
        useremail = db.execute("SELECT email FROM REGISTER WHERE email=:email", {"email":email}).fetchone()
        if useremail == None:
            return render_template("page-register.html")
        else:
            return render_template("index.html")
    return render_template('page-forgot-password.html')

if __name__ == '__main__':
    app.secret_key="kulksidtestkey"
    app.run(debug=True)