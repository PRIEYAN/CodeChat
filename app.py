from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import join_room, leave_room, send, SocketIO
import random

app = Flask(__name__) 
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login.db"
app.config['SECRET_KEY'] = "FDSFSDSFDSHJFDSIFHDSFHDSIFH"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    usrid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

rooms = {}

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
        existing_mail = Users.query.filter_by(email=email).first()
        if existing_user:
            finnalMsg = "*User already exists!"
            return render_template('signup.html', finnalMsg=finnalMsg)
        elif existing_mail:
            finnalMsg = "*Mail ID already exists"
            return render_template('signup.html', finnalMsg=finnalMsg)
        else:
            new_user = Users(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username  # Save username in session
            return render_template('login.html')
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email, password=password).first()
        if user:
            session['username'] = user.username
            return render_template('Userapp.html')
        else:
            finnalMsg = '*Check the email or password'
            return render_template('login.html', finnalMsg=finnalMsg)
    return render_template("login.html")

@app.route('/app')
def theapp():
    randm = int(random.uniform(1000, 9999))
    name = session.get('username', ' ')
    return render_template('Userapp.html', randm=randm, name=name)

@app.route('/room', methods=['POST', 'GET'])
def room():
    return render_template('room.html')
# Socket.IO Event for handling users joining a room
@socketio.on('join')
def on_join(data):
    username = session.get('username', 'Anonymous')  # Default to 'Anonymous' if not logged in
    room = data['room']
    join_room(room)
    send({'name': username, 'message': f'blud joined the room!'}, to=room)

# Socket.IO Event for handling message sending
@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')  # Get the username from the session or default to 'Anonymous'
    room = data['room']
    message = data['message']
    send({'name': username, 'message': message}, to=room)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5050)
