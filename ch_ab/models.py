from email.policy import default
from enum import unique
from ssl import _create_unverified_context
from ch_ab import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol


@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))


user_request=db.Table('user_request',
                db.Column('u_id',db.Integer,db.ForeignKey('login.id')),
                db.Column('r_id',db.Integer,db.ForeignKey('issue_response.id')))




class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    usertype = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(200),default='NULL')
    name = db.Column(db.String(200))
    address= db.Column(db.VARCHAR)
    contact= db.Column(db.String(200))
    cls= db.Column(db.String(200))
    division= db.Column(db.String(200))
    category= db.Column(db.String(200))
    gender= db.Column(db.String(200))
    offaddress= db.Column(db.String(200))
    qualification= db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    

    
class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    uid = db.Column(db.String(200))
    email= db.Column(db.VARCHAR)
    contact= db.Column(db.VARCHAR)
    subject= db.Column(db.VARCHAR)
    message= db.Column(db.String(200))


    
class Booking(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80))
    cid = db.Column(db.String(80))
    status = db.Column(db.String(200),default='Waiting for Confirmation')
    uname = db.Column(db.String(200))
    uaddress= db.Column(db.VARCHAR)
    ucontact= db.Column(db.String(200))
    uemail = db.Column(db.String(200))
    uclass= db.Column(db.String(200))
    udivision= db.Column(db.String(200))
    ucategory= db.Column(db.String(200))
    ugender= db.Column(db.String(200))
    cname = db.Column(db.String(200))
    caddress= db.Column(db.VARCHAR)
    ccontact= db.Column(db.String(200))
    cemail = db.Column(db.String(200))
    coffaddress = db.Column(db.String(200))
    date= db.Column(db.VARCHAR)
    time= db.Column(db.String(200))
 
class Issue(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(200))
    tid = db.Column(db.String(200))
    accept_id = db.Column(db.String(200))
    usertype= db.Column(db.VARCHAR)
    subject= db.Column(db.VARCHAR)
    issue= db.Column(db.VARCHAR)
    solution= db.Column(db.String(200))
    name = db.Column(db.String(200))
    address= db.Column(db.VARCHAR)
    contact= db.Column(db.String(200))
    cls= db.Column(db.String(200))
    division= db.Column(db.String(200))
    category= db.Column(db.String(200))
    gender= db.Column(db.String(200))
    status = db.Column(db.String(200),default='NULL')
    progress= db.Column(db.String(200))
    permisson= db.Column(db.String(200))


class Issue_response(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    issue_id = db.Column(db.String(200))
    respond_id = db.relationship('Login',secondary=user_request,backref='tests')
    status_res = db.Column(db.String(200),default='NULL')
    response= db.Column(db.VARCHAR)
    progress= db.Column(db.String(200))
  


class C_solution(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(200))
    tid = db.Column(db.String(200))
    issue_id = db.Column(db.String(200))
    cid = db.Column(db.String(200))
    uname= db.Column(db.VARCHAR)
    uaddress= db.Column(db.VARCHAR)
    ucontact= db.Column(db.String(200))
    ucategory= db.Column(db.String(200))
    ugender= db.Column(db.String(200))
    cname = db.Column(db.String(200))
    caddress= db.Column(db.VARCHAR)
    ccontact= db.Column(db.String(200))
    cemail = db.Column(db.String(200))
    coffaddress = db.Column(db.String(200))
    subject= db.Column(db.VARCHAR)
    issue= db.Column(db.VARCHAR)
    solution= db.Column(db.String(200))
    usertype= db.Column(db.String(200))
    type= db.Column(db.String(200))
    status = db.Column(db.String(200),default='NULL')
    