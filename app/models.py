from datetime import datetime
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_sqlalchemy import SQLAlchemy

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

# User database
class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ownedcases = db.relationship('Cases', backref='casecreator', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

# Case database
class Cases(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    casename = db.Column(db.String)
    creator = db.Column(db.String)
    createdate = db.Column(db.String)
    status = db.Column(db.Integer)
    flashpoint = db.Column(db.Integer)
    crowdstrike = db.Column(db.Integer)
    postgres = db.Column(db.Integer)
    virustotal = db.Column(db.Integer)
    polyswarm = db.Column(db.Integer)
    googlecse = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, casename, creator, createdate, status, flashpoint, crowdstrike, postgres, virustotal, polyswarm, googlecse, user_id):
        self.casename = casename
        self.creator = creator
        self.createdate = createdate
        self.status = status
        self.flashpoint = flashpoint
        self.crowdstrike = crowdstrike
        self.postgres = postgres
        self.virustotal = virustotal
        self.polyswarm = polyswarm
        self.googlecse = googlecse
        self.user_id = user_id

class SlackWebhook(db.Model):
    __tablename__ = 'slackwebhook'

    id = db.Column(db.Integer, primary_key=True)
    slackwebhook = db.Column(db.String, nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, slackwebhook, caseid):
        self.slackwebhook = slackwebhook
        self.caseid = caseid

# IOC databases
class Names(db.Model):
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String, nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Usernames(db.Model):
    __tablename__ = 'usernames'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String, nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class UserIDs(db.Model):
    __tablename__ = 'userids'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.Integer, nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Emails(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Phones(db.Model):
    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.Integer, nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class IPaddresses(db.Model):
    __tablename__ = 'ipaddresses'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(24), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Keywords(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Domains(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Urls(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class BTCAddresses(db.Model):
    __tablename__ = 'btcaddresses'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Sha256(db.Model):
    __tablename__ = 'sha256'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Sha1(db.Model):
    __tablename__ = 'sha1'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Md5(db.Model):
    __tablename__ = 'md5'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class Filenames(db.Model):
    __tablename__ = 'filename'

    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(120), nullable=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, indicator, caseid):
        self.indicator = indicator
        self.caseid = caseid

class IOCMatches(db.Model):
    __tablename__ = 'iocmatches'

    id = db.Column(db.Integer, primary_key=True)
    osintgoogle = db.Column(db.Text)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, osintgoogle, caseid):
        self.osintgoogle = osintgoogle
        self.caseid = caseid

class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    author = db.Column(db.String(32))
    createdate = db.Column(db.String)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, text, author, createdate, caseid):
        self.text = text
        self.author = author
        self.createdate = createdate
        self.caseid = caseid

class Events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    indicator = db.Column(db.String(255))
    event = db.Column(db.Text)
    platform = db.Column(db.String)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id"))

    def __init__(self, time, indicator, event, platform, caseid):
        self.time = time
        self.indicator = indicator
        self.event = event
        self.platform = platform
        self.caseid = caseid