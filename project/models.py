from project import db
from datetime import datetime
from sqlalchemy import and_, or_
from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id                  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username            = db.Column(db.String, unique=True, nullable=False)
    displayname         = db.Column(db.String)
    #email               = db.Column(db.String, unique=True, nullable=False)
    bio                 = db.Column(db.String, default = "Hi, i'm using Artflict!")
    profile_pic_url     = db.Column(db.String, nullable=True)
    password_hash       = db.Column(db.String, nullable=False)
    def __init__(self, username, displayname, password):
        self.username = username
        self.displayname = displayname
        self.set_password(password)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_followers(self):
        get_followers = Follower.query.filte_by(followedID = self.id)
        return get_followers
    def get_followed(self):
        get_followed = Follower.query.filte_by(followerID = self.id)
        return get_followed
    def __repr__(self):
        return 'User %d %s' % (self.id, self.username)
class Post(db.Model):
    __tablename__='posts'
    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AuthorID       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ArtURL         = db.Column(db.String)
    ArtistID       = db.Column(db.Integer, db.ForeignKey('users.id'))
    ArtistNotes    = db.Column(db.String)
    Title          = db.Column(db.String(20), nullable=False)
    Text           = db.Column(db.String, nullable=False)
    Rating         = db.Column(db.Integer)
    Date           = db.Column(db.String, nullable=False)
    def __init__(self, AuthorID, Title, Text):
        self.AuthorID = AuthorID
        self.Title = Title
        self.Text = Text
        self.Date = self.format_date()
        self.Rating = 0
    def relate(self):
        userid = current_user.id
        getpostlike = Like.query.filter_by(postID = self.id).filter_by(userID = userid).first()
        if getpostlike:
            db.session.delete(getpostlike)
        else:
            add_like = Like(userid, self.id)
            db.session.add(add_like)
        db.session.commit()
        getlikes = Like.query.filter_by(postID = self.id).all()
        self.Rating = len(getlikes)
    def format_rating(self):
        rating = float(self.Rating)
        if rating < 1000:
            return str(rating)
        elif rating < 1000000:
            new_rating = round(rating / 1000, 1)
            return  new_rating + "K"
        elif rating < 1000000000:
            new_rating = round(rating / 1000000, 1)
            return new_rating + "M"
        else:
            return "LOTS"
    def format_date(self):
        now = datetime.now()
        month_dict = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July',
                        8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        month = month_dict[now.month][:3]
        day_suffix = {1:'st', 2:'nd'}
        if now.day < 3:
            day = str(now.day) + day_suffix[now.day]
        else:
            day = str(now.day) + 'th'
        return month + " " + day + " " + str(now.year)
    def __repr__(self):
        return "post " + str(self.id) + " " + str(self.Title) + " " + str(self.Text)
class Like(db.Model):
    __tablename__='likes'
    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    postID         = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    def __init__(self, userID, postID):
        self.userID = userID
        self.postID = postID
    def __repr__(self):
        return "like " + str(self.id) + " " + str(self.userID) + " " + str(self.postID)
class Follower(db.Model):
    __tablename__ = 'followers'
    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    followerID     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followedID     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __init__(self, followerID, followedID):
         self.followerID = followerID
         self.followedID = followedID
    def __repr__(self):
        return "like " + str(self.id) + " " + str(self.followerID) + " " + str(self.followedID)