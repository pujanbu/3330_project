# db models for bolchal

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


# relationship between page and profile where profile is admin of page
admins = db.Table('admins', db.Column('page_id', db.Integer, db.ForeignKey('page.id', ondelete='CASCADE')),
                  db.Column('profile_id', db.Integer, db.ForeignKey('profile.id', ondelete='CASCADE')))


# relationship between page and profile where profile is member of page
members = db.Table('members', db.Column('page_id', db.Integer, db.ForeignKey('page.id', ondelete='CASCADE')),
                   db.Column('profile_id', db.Integer, db.ForeignKey('profile.id', ondelete='CASCADE')))


class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    # relations
    posts = db.relationship("Post", backref="profile",
                            lazy=True, cascade='all,delete')
    like = db.relationship("Like", backref="profile", lazy=True)

    def __init__(self, first_name, last_name, email, username, password, mobile_no=""):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.mobile_no = mobile_no

    def __repr__(self):
        return f'<Profile {self.username}>'

    def __str__(self):
        return f'{self.username}'


class Page(db.Model):
    __tablename__ = "page"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    desc = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    views = db.Column(db.Integer, default=0)

    # relations
    posts = db.relationship("Post", backref="page", lazy=True)
    likes = db.relationship("Like", backref="page", lazy=True)
    admins = db.relationship("Profile", secondary=admins,
                             lazy=True, backref=db.backref('adminof', lazy=True))
    members = db.relationship("Profile", secondary=members,
                              lazy=True, backref=db.backref('memberof', lazy=True))

    def __init__(self, name, desc, category=""):
        self.name = name
        self.desc = desc
        self.category = category


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String(10), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    # relationships
    comments = db.relationship("Comment", backref="post", lazy=True)
    likes = db.relationship("Like", backref="post", lazy=True)
    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profile.id", ondelete='CASCADE'))
    page_id = db.Column(db.Integer, db.ForeignKey(
        "page.id", ondelete='CASCADE'))

    def __init__(self, post_type, body, profile_id, page_id):
        self.post_type = post_type
        self.body = body
        if profile_id:
            self.profile_id = profile_id
        else:
            self.page_id = page_id


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    # relations
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post.id", ondelete='CASCADE'))
    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profile.id", ondelete='CASCADE'))
    page_id = db.Column(db.Integer, db.ForeignKey(
        "page.id", ondelete='CASCADE'))

    def __init__(self, body, post_id, profile_id, page_id):
        self.body = body
        self.post_id = post_id
        if profile_id:
            self.profile_id = profile_id
        else:
            self.page_id = page_id


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    # relations
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post.id", ondelete='CASCADE'))
    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profile.id", ondelete='CASCADE'))
    page_id = db.Column(db.Integer, db.ForeignKey(
        "page.id", ondelete='CASCADE'))

    def __init__(self, post_id, profile_id, page_id):
        self.post_id = post_id
        if profile_id:
            self.profile_id = profile_id
        else:
            self.page_id = page_id
