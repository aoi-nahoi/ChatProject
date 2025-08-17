from app import login_manager, db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    hobby = db.Column(db.String)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key = True)
    from_ = db.Column(db.Integer, unique=False, nullable=False) #メッセージの送信者
    to_ = db.Column(db.Integer, unique=False, nullable=False) #メッセージの受信者
    body = db.Column(db.String) #メッセージ内容
    timestanp = db.Column(db.DateTime, default=db.func.now()) #メッセージの送信時間