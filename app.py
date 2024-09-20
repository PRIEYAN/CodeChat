from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    usrid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()
@app.route('/')
def main():
    return render_template("index.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = Users.query.filter_by(username=username).first()
        existing_mail=Users.query.filter_by(email=email).first()
        if existing_user:
            finnalMsg = "*User already exists!"
            return render_template('signup.html', finnalMsg=finnalMsg)
        elif existing_mail:
            finnalMsg="*Mail ID already exists"
            return render_template('signup.html',finnalMsg=finnalMsg)
        else:
            new_user = Users(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html',)
    return render_template('signup.html')





@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Query for the user with matching email and password
        user = Users.query.filter_by(email=email, password=password).first()

        if user:
            return render_template('Userapp.html',username=user)
        else:
            finnalMsg = '*Check the email or password'
            return render_template('login.html', finnalMsg=finnalMsg)
    
    return render_template("login.html")

@app.route('/app')
def theapp():
    return render_template('Userapp.html',)



if __name__ == "__main__":
    app.run(debug=True,port=5555)
