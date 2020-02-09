import datetime
from app import db


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)

    command = db.Column(db.String(32))
    made_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_from = db.relationship('User', foreign_key='user_from_id')

    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_to = db.relationship('User', foreign_key='user_to_id')

    hardcopy_id = db.Column(db.Integer, db.ForeignKey('hardcopies.id'))
    hardcopy = db.relationship('Hardcopy')
