from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship

ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email_id = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150))
    #meeting = db.relationship('Meeting', backref="meetings", passive_deletes='all')

    def __init__(self, email_id, name):
        self.email_id = email_id
        self.name = name

class UserSchema(ma.Schema):
    id = fields.Integer()
    email_id = fields.Email(required=True)
    name = fields.String(required=False)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer,primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id",  ondelete='CASCADE'), nullable=False)
    meeting_date = db.Column(db.DateTime)
    users = relationship(User, backref=backref('users', cascade='delete, all'))
    def __init__(self, host_id):
        self.host_id = host_id

class MeetingSchema(ma.Schema):
    id = fields.Integer()
    host_id = fields.Integer(required=True)
    meeting_date = fields.DateTime() 

class Recording(db.Model):
    __tablename__ = 'recordings'
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    length = db.Column(db.Integer())
    md5_hash = db.Column(db.String(128))
    private = db.Column(db.Boolean)
    meeting_id =  db.Column(db.Integer,  db.ForeignKey('meetings.id', ondelete='CASCADE'), nullable=False)
    meetings = relationship(Meeting, backref=backref('meetings', cascade='delete, all'))


    def __init__(self, url, md5_hash, length, meeting_id, private):
        self.url = url
        self.length = length
        self.private = private
        self.md5_hash = md5_hash
        self.meeting_id = meeting_id

class RecordingSchema(ma.Schema):
    id = fields.Integer()
    url = fields.Url(required=True)
    length = fields.Integer(required=False)
    md5_hash = fields.String(required=False)
    private = fields.Boolean(required=False)
    meeting_id = fields.Integer(required=True)


class ViewRecording(db.Model):
    __tablename__ = 'view_recordings'
    recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id', ondelete='CASCADE'), primary_key=True)
    recordings = relationship(Recording, backref=backref('recordings', cascade='delete, all'))  
    email_id = db.Column(db.String(150), primary_key=True)
    
    def __init__(self, email_id, recording_id):
        self.email_id = email_id
        self.recording_id = recording_id

class ViewRecordingSchema(ma.Schema):
    recording_id = fields.Integer()
    email_id = fields.Email(required=True)

