from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    passwords = db.relationship('Password', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_attribute = db.Column(db.String(120), index=True)
    password_account = db.Column(db.String(120), index=True)
    password_body = db.Column(db.String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<password attribute: {}, password account: {}, password body: {}>'.format(self.password_attribute, self.password_account, self.password_body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
