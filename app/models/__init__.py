from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'<Role {self.id}: {self.name}>'
