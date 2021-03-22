from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from passlib.hash import sha256_crypt

engine = create_engine("sqlite:///test.db")
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

#register
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        securepass = sha256_crypt.encrypt(str(password))

        if password == cpassword:
            db.execute("INSERT into REGISTER(username, email, password) VALUES(:name, :email, :password)", {"name":name, "email":email, "password":securepass})
            db.commit()
            flash("Account created!", "success")
            return redirect(url_for('login'))
        else:
            flash("password doesn't match", "danger")
            return render_template("register.html")
    return render_template('register.html')

#login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT username FROM REGISTER WHERE username=:username", {"username":username}).fetchone()
        passwordata = db.execute("SELECT password FROM REGISTER WHERE username=:username", {"username":username}).fetchone()

        if usernamedata is None:
            flash("No user found!", "danger")
            return render_template("login.html")
        else:
            for pass_data in passwordata:
                if sha256_crypt.verify(password, pass_data):
                    flash("Login successful!", "success")
                    return redirect(url_for('dash'))
                else:
                    flash("Incorrect Password", "danger")
                    return render_template("login.html")

    return render_template('login.html')

@app.route('/dash')
def dash():
    return render_template("dash.html")

if __name__ == '__main__':
    app.secret_key="kulksidtestkey"
    app.run(debug=True)