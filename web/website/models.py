from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #date = db.Column(db.DateTime(timezone=True), default=func.now())
    date = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#azért pici az u mert sql így nézi de ez User

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(500))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #flask + sql bele rak noteid-t, hogy az összeshez hozzáférjünk