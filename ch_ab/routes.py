from msilib.schema import File
from unicodedata import category
from flask import Flask, render_template, request, redirect,send_file,  flash, abort, url_for
from ch_ab import app,db,mail
from ch_ab import app,db,mail
from ch_ab import app
from ch_ab.models import *

from flask_login import login_user, logout_user, login_required,current_user
from random import randint
import os
from PIL import Image
from flask_mail import Message
from io import BytesIO
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from datetime import datetime as dt
from datetime import datetime,date
# from datetime import timedelta
from werkzeug.utils import secure_filename


from datetime import datetime, timedelta
from sqlalchemy import and_
# from parser import issuite






@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template("about.html")



@app.route('/services',methods=['GET', 'POST'])
def services():
    return render_template("services.html")




@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        admin = Login.query.filter_by(username=username, password=password,usertype= 'admin').first()
        counsellor=Login.query.filter_by(username=username,password=password, usertype= 'counsellor',status="approve").first()
        user=Login.query.filter_by(username=username,password=password, usertype= 'user').first()
        teacher=Login.query.filter_by(username=username,password=password, usertype= 'teacher').first()
        if admin:
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin_index') 
             
        elif counsellor:
            login_user(counsellor)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/c_index/'+str(counsellor.id))
         
        elif user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/user_index/'+str(user.id))

        elif teacher:
            login_user(teacher)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/t_index/'+str(teacher.id)) 
         
        else:
            d="Invalid Username or Password" 
            return render_template("login.html",d=d)
  
    return render_template("login.html")



@app.route('/reg_user',methods=['GET', 'POST'])
def reg_user():
    if request.method == 'POST':
        
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        cls = request.form['cls']
        division = request.form['division']
        category = request.form['category']
        gender = request.form['gender']
        my_data1 = Login(name=name,address=address,username=email,contact=contact,password=password,cls=cls,division=division,category=category,gender=gender,usertype="user")
        db.session.add(my_data1) 
        db.session.commit()
       
       
        return redirect('/login')
        
    else :
        return render_template("reg_user.html")
    

@app.route('/reg_counslr',methods=['GET', 'POST'])
def reg_counslr():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        offaddress = request.form['offaddress']
        qualification = request.form['qualification']
        category = request.form['category']
        img=request.files['image']
        pic_file = save_picture(img)
        view = pic_file
        print(view) 
        my_data1 = Login(name=name,image=view,address=address,username=email,contact=contact,password=password,offaddress=offaddress,category=category,qualification=qualification,usertype="counsellor")
        db.session.add(my_data1)
        db.session.commit()
       
        d="Registered successfully! Please waiting for the Confirmation.."
        return render_template("reg_counslr.html",d=d)
        
    else :
        return render_template("reg_counslr.html")
    


@app.route('/reg_tchr',methods=['GET', 'POST'])
def reg_tchr():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        cls = request.form['cls']
        division = request.form['division']
        
        my_data1 = Login(name=name,address=address,username=email,contact=contact,cls=cls,division=division,password=password,usertype="teacher")
        db.session.add(my_data1) 
        db.session.commit()
       
       
        return redirect('/login')
        
    else :
        return render_template("reg_tchr.html")




def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)






@app.route('/c_index/<cid>')
@login_required
def c_index(cid):
    return render_template("c_index.html")


@app.route('/user_index/<id>')
@login_required
def user_index(id):
    return render_template("user_index.html")


@app.route('/t_index/<id>')
@login_required
def t_index(id):
    return render_template("t_index.html")



@app.route('/admin_index')
@login_required
def admin_index():
    return render_template("admin_index.html")

@app.route('/layout',methods=['GET', 'POST'])
def layout():
    return render_template("layout.html")

@app.route('/admin_layout',methods=['GET', 'POST'])
def admin_layout():
    return render_template("admin_layout.html")

@app.route('/user_layout',methods=['GET', 'POST'])
def user_layout():
    return render_template("user_layout.html")



@app.route('/t_layout',methods=['GET', 'POST'])
def t_layout():
    return render_template("t_layout.html")


@app.route('/c_layout',methods=['GET', 'POST'])
def c_layout():
    return render_template("c_layout.html")




@app.route('/admin_vw_user')
@login_required
def admin_vw_user():
    obj = Login.query.filter_by(usertype="user").all()
    return render_template("admin_vw_user.html",obj=obj)





@app.route('/admin_vw_tchrs')
@login_required
def admin_vw_tchrs():
    obj = Login.query.filter_by(usertype="teacher").all()
    return render_template("admin_vw_tchrs.html",obj=obj)

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route('/admin_vw_c_req')
@login_required
def admin_vw_c_req():
    obj=Login.query.filter_by(usertype="counsellor",status="NULL").all()
    return render_template("admin_vw_c_req.html",obj=obj)



@app.route('/app_counslr/<int:id>')
@login_required
def app_counslr(id):
    c= Login.query.get_or_404(id)
    c.status = 'approve'
    db.session.commit()
    a_sendmail(c.username)
    return redirect('/admin_app_counslr')





@app.route('/rej_counslr/<int:id>')
@login_required
def rej_counslr(id):
    c= Login.query.get_or_404(id)
    c.status = 'reject'
    db.session.commit()
    r_sendmail(c.username)
    return redirect('/admin_rej_counslr')


def a_sendmail(username):
    msg = Message('Approved Successfully',
                  recipients=[username])
    msg.body = f''' Congratulations , Your  Registeration is approved successfully... Now You can login using username and password '''
    mail.send(msg)

def r_sendmail(username):
    msg = Message('Registeration Rejected',
                  recipients=[username])
    msg.body = f''' Sorry , Your  Registeration is rejected. '''
    mail.send(msg)



@app.route('/admin_app_counslr')
@login_required
def admin_app_counslr():
    obj=Login.query.filter_by(usertype="counsellor",status="approve").all()
    return render_template("admin_app_counslr.html",obj=obj)




@app.route('/admin_rej_counslr')
@login_required
def admin_rej_counslr():
    obj=Login.query.filter_by(usertype="counsellor",status="reject").all()
    return render_template("admin_rej_counslr.html",obj=obj)


@app.route('/user_profile/<id>')
@login_required
def user_profile(id):
    d= Login.query.get_or_404(id)
    return render_template("user_profile.html",d=d)



@app.route('/c_profile/<id>')
@login_required
def c_profile(id):
    d= Login.query.get_or_404(id)
    return render_template("c_profile.html",d=d)


@app.route('/t_profile/<id>')
@login_required
def t_profile(id):
    d= Login.query.get_or_404(id)
    return render_template("t_profile.html",d=d)

@app.route('/user_profile_update/<int:id>',methods=['GET', 'POST'])
@login_required
def user_profile_update(id):
    d = Login.query.filter_by(id=id).first()
   
    if request.method == 'POST':
        d.name = request.form['name']
        d.address = request.form['address']
        d.username = request.form['email']
        d.contact = request.form['contact']
        d.password = request.form['password']
        d.cls = request.form['cls']
        d.division = request.form['division']
        d.category = request.form['category']
        d.gender = request.form['gender']
        db.session.commit()
        return redirect('/user_profile/'+str(d.id))
        
    else :
        return render_template("user_profile_update.html",d=d)




@app.route('/t_profile_update/<int:id>',methods=['GET', 'POST'])
@login_required
def t_profile_update(id):
    d = Login.query.filter_by(id=id).first()
   
    if request.method == 'POST':
        d.name = request.form['name']
        d.address = request.form['address']
        d.username = request.form['email']
        d.contact = request.form['contact']
        d.password = request.form['password']
        
        db.session.commit()
        return redirect('/t_profile/'+str(d.id))
        
    else :
        return render_template("t_profile_update.html",d=d)


@app.route('/c_profile_update/<int:id>',methods=['GET', 'POST'])
@login_required
def c_profile_update(id):
    d = Login.query.filter_by(id=id).first()
   
    if request.method == 'POST':
        d.name = request.form['name']
        d.address = request.form['address']
        d.username = request.form['username']
        d.contact = request.form['contact']
        d.password = request.form['password']
        d.offaddress = request.form['offaddress']
        d.qualification = request.form['qualification']
        db.session.commit()
        return redirect('/c_profile/'+str(d.id))
        
    else :
        return render_template("c_profile_update.html",d=d)



@app.route('/user_view_counslr')
@login_required
def user_view_counslr():
    search=request.args.get('search')
    if search:
        obj=Login.query.filter((Login.name.contains(search)|Login.qualification.contains(search)|Login.address.contains(search)|Login.offaddress.contains(search)) & Login.usertype.contains("counsellor")  & Login.status.contains("approve"))
    else:
        obj= Login.query.filter_by(usertype="counsellor",status="approve").all()
    
    return render_template("user_view_counslr.html",obj=obj)





@app.route('/t_view_counslr')
@login_required
def t_view_counslr():
    search=request.args.get('search')
    if search:
        obj=Login.query.filter((Login.name.contains(search)|Login.qualification.contains(search)|Login.address.contains(search)|Login.offaddress.contains(search)) & Login.usertype.contains("counsellor")  & Login.status.contains("approve"))
    else:
        obj= Login.query.filter_by(usertype="counsellor",status="approve").all()
    
    return render_template("t_view_counslr.html",obj=obj)



@app.route('/user_book_counslr/<int:cid>',methods=['GET', 'POST'])
@login_required
def user_book_counslr(cid):
    
    b=Login.query.filter_by(id=cid).first()
    a=Login.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        uname = request.form['uname']
        uaddress = request.form['uaddress']
        uemail = request.form['uemail']
        ucontact = request.form['ucontact']
        ucategory = request.form['ucategory']
        ugender = request.form['ugender']
        uclass = request.form['uclass']
        udivision = request.form['udivision']
        cname = request.form['cname']
        cemail = request.form['cemail']
        caddress = request.form['caddress']
        ccontact = request.form['ccontact']
        coffaddress = request.form['coffaddress']
        date = request.form['date']
        time = request.form['time']
        my_data1 = Booking(uid=current_user.id,cid=b.id,uname=uname,uaddress=uaddress,ucategory=ucategory,ugender=ugender,uemail=uemail,ucontact=ucontact,uclass=uclass,udivision=udivision,cname=cname,caddress=caddress,cemail=cemail,ccontact=ccontact,date=date,time=time,coffaddress=coffaddress)
        db.session.add(my_data1)
        db.session.commit()
        return redirect('/user_view_booking/'+str(a.id))

    return render_template("user_book_counslr.html",a=a,b=b)



@app.route('/user_view_booking/<id>')
@login_required
def user_view_booking(id):
    obj= Booking.query.filter_by(uid=id).all()
    return render_template("user_view_booking.html",obj=obj)



@app.route('/c_view_booking/<id>')
@login_required
def c_view_booking(id):
    obj= Booking.query.filter_by(cid=id,status="Waiting for Confirmation").all()
    return render_template("c_view_booking.html",obj=obj)



@app.route('/c_app_booking/<int:id>')
@login_required
def c_app_booking(id):
    c= Booking.query.get_or_404(id)
    c.status = 'approved'
    db.session.commit()
    app_sendmail(c.uemail)
    return redirect('/c_approved_user/'+str(c.cid))



@app.route('/c_reject_booking/<int:id>')
@login_required
def c_reject_booking(id):
    c= Booking.query.get_or_404(id)
    c.status = 'rejected'
    db.session.commit()
    rej_sendmail(c.uemail)
    return redirect('/admin_rej_counslr')


def app_sendmail(uemail):
    msg = Message('Approved Successfully',
                  recipients=[uemail])
    msg.body = f''' Congratulations , Your  Booking for the Consultation approved successfully...  '''
    mail.send(msg)

def rej_sendmail(uemail):
    msg = Message('Registeration Rejected',
                  recipients=[uemail])
    msg.body = f''' Sorry , Your  Booking is rejected. '''
    mail.send(msg)



@app.route('/c_approved_user/<id>')
@login_required
def c_approved_user(id):
    obj= Booking.query.filter_by(cid=id,status="approved").all()
    return render_template("c_approved_user.html",obj=obj)


@app.route('/user_add_issue/<int:id>',methods=['GET', 'POST'])
@login_required
def user_add_issue(id):
    d = Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        subject = request.form['subject']
        issue = request.form['issue']
        my_data1 = Issue(uid=id,subject=subject,issue=issue,contact=d.contact,usertype=d.usertype,category=d.category,
        name=d.name,address=d.address,cls=d.cls,division=d.division,gender=d.gender)
        db.session.add(my_data1) 
        db.session.commit()
        return redirect('/user_view_issue/'+str(id))
        
    else :
        return render_template("user_add_issue.html",d=d)



@app.route('/c_vw_issue/<int:id>')
@login_required
def c_view_issue(id):
    a=Login.query.filter_by(id=current_user.id).first()
    if  a.category == "police" :

        obj= Issue.query.filter_by(status="police").all()
        return render_template("c_vw_issue.html",obj=obj)
        
    else:

        obj= Issue.query.filter_by(status="doctor").all()
        return render_template("c_vw_issue.html",obj=obj)


@app.route('/p_d_accept/<int:id>',methods=['GET', 'POST'])
@login_required
def police_accept(id):
    a=Login.query.filter_by(id=current_user.id).first()
    if  a.category == "police" :

            d = Issue.query.filter_by(id=id).first()
            d.status = 'p_accept'
            d.accept_id=current_user.id
            db.session.commit()
            return redirect('/c_vw_issue/'+str(id))
    else:

         
            d = Issue.query.filter_by(id=id).first()
            d.status = 'd_accept'
            d.accept_id=current_user.id
            db.session.commit()
            return redirect('/c_vw_issue/'+str(id))
    return redirect('/c_vw_issue/'+str(id))

       


@app.route('/po_acc_issue/<int:id>')
@login_required
def police_acc_issue(id):

    obj= Issue.query.filter_by(accept_id=current_user.id).all()
    return render_template("po_acc_issue.html",obj=obj)



@app.route('/user_view_issue/<int:id>')
@login_required
def user_vw_issue(id):
    
    obj = Issue.query.filter_by(uid=current_user.id).all()
    return render_template("user_view_issue.html",obj=obj)
    # return redirect('/login')
 


@app.route('/admin_vw_issue')
@login_required
def admin_view_issue():
    obj= Issue.query.filter_by(category="parent",status="NULL").all()
    return render_template("admin_vw_issue.html",obj=obj)


@app.route('/p_history')
@login_required
def parent_history():
    obj= Issue.query.filter_by(category="parent",status="complete").all()
    return render_template("p_history.html",obj=obj)



@app.route('/s_history')
@login_required
def student_history():
    obj= Issue.query.filter_by(category="student",status="complete").all()
    return render_template("s_history.html",obj=obj)




@app.route('/ad_vw_issue')
@login_required
def ad_view_issue():
    obj= Issue.query.filter_by(status ="escalate").all()
    return render_template("ad_vw_issue.html",obj=obj)



@app.route('/t_vw_issues')
@login_required
def t_view_issues():
    obj= Issue.query.filter_by(category="student",status="NULL").all()
    return render_template("t_vw_issues.html",obj=obj)


@app.route('/t_history')
@login_required
def t_vw_history():
    obj= Issue.query.filter_by(category="student",status="complete").all()
    return render_template("t_history.html",obj=obj)


    

@app.route('/view_response/<int:id>')
@login_required
def vw_response(id):

    try:
        r = Issue_response.query.filter_by(issue_id=id).all()
        for i in r:
            c=Issue.query.filter_by(id=i.issue_id).first()
        return render_template("view_response.html",c=c,r=r)
    except:
        t="No Response"
        return render_template("view_response.html",t=t)
        
    
   
@app.route('/res_teacher/<int:id>',methods=['GET', 'POST'])
@login_required
def response_t(id):
    d = Issue.query.filter_by(id=id).first()
    f= Login.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        issue_id=d.id
        response = request.form['response']
        status_res = request.form['status_res']
        progress = request.form['progress']
        my_data1 = Issue_response(response=response,issue_id=issue_id,respond_id=[f],status_res=status_res,progress=progress)
        if progress =='100%' :
            d.status = 'complete'
            db.session.commit()
        db.session.add(my_data1) 
        db.session.commit()
        return redirect('/t_vw_issues/'+str(id))
        
    else :
        return render_template("res_teacher.html",d=d)



@app.route('/po_response/<int:id>',methods=['GET', 'POST'])
@login_required
def p_d_response(id):
    d = Issue.query.filter_by(id=id).first()
    f= Login.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        issue_id=d.id
        response = request.form['response']
        status_res = request.form['status_res']
        progress = request.form['progress']
        my_data1 = Issue_response(response=response,issue_id=issue_id,respond_id=[f],status_res=status_res,progress=progress)
        if progress =='100%' :
            d.status = 'complete'
            db.session.commit()
       
        db.session.add(my_data1) 
        db.session.commit()
        return redirect('/po_acc_issue/'+str(id))
        
    else :
        return render_template("po_response.html",d=d)




@app.route('/es_teacher/<int:id>',methods=['GET', 'POST'])
@login_required
def escalate_teacher(id):
    d = Issue.query.filter_by(id=id).first()
    d.status = 'escalate'
    db.session.commit()
    return redirect('/t_vw_issues/'+str(id))
        
@app.route('/status_police/<int:id>',methods=['GET', 'POST'])
@login_required
def status_p(id):
    d = Issue.query.filter_by(id=id).first()
    d.status = 'police'
    db.session.commit()
    return redirect('/admin_vw_issue')


@app.route('/status_doctor/<int:id>',methods=['GET', 'POST'])
@login_required
def status_dr(id):
    d = Issue.query.filter_by(id=id).first()
    d.status = 'doctor'
    db.session.commit()
    return redirect('/admin_vw_issue')






@app.route('/his_res_te/<int:id>')
@login_required
def history_res_te(id):

    try:
        r = Issue_response.query.filter_by(issue_id=id).all()
        for i in r:
            c=Issue.query.filter_by(id=i.issue_id).first()
        return render_template("his_res_te.html",c=c,r=r)
    except:
        t="No Response"
        return render_template("his_res_te.html",t=t)
  

@app.route('/his_res_p/<int:id>')
@login_required
def history_res_pa(id):

    try:
        r = Issue_response.query.filter_by(issue_id=id).all()
        for i in r:
            c=Issue.query.filter_by(id=i.issue_id).first()
        return render_template("his_res_p.html",c=c,r=r)
    except:
        t="No Response"
        return render_template("his_res_p.html",t=t)
  


@app.route('/his_res_d/<int:id>')
@login_required
def history_res_do(id):

    try:
        r = Issue_response.query.filter_by(issue_id=id).all()
        for i in r:
            c=Issue.query.filter_by(id=i.issue_id).first()
        return render_template("his_res_d.html",c=c,r=r)
    except:
        t="No Response"
        return render_template("his_res_d.html",t=t)
  

@app.route('/c_contact/<int:id>',methods=['GET', 'POST'])
@login_required
def c_contact(id):
    d = Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        contact = request.form['contact']
        message = request.form['message']
        my_data1 = Contact(uid=d.id,name=name,email=email,message=message,subject=subject,contact=contact)
        db.session.add(my_data1) 
        db.session.commit()
        return redirect('/c_index/'+str(d.id))
        
    return render_template("c_contact.html",d=d)

@app.route('/contact',methods=['GET', 'POST'])
def p_contact () :
   
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        contact = request.form['contact']
        message = request.form['message']
        my_data1 = Contact(name=name,email=email,message=message,subject=subject,contact=contact)
        db.session.add(my_data1) 
        db.session.commit()
        return redirect('/')
        
    return render_template("contact.html")




@app.route('/user_contact/<int:id>',methods=['GET', 'POST'])
@login_required
def user_contact(id):
    d = Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        subject = request.form['subject']
        message = request.form['message']
        my_data1 = Contact(uid=d.id,name=name,email=email,message=message,subject=subject,contact=contact)
        db.session.add(my_data1) 
        db.session.commit()
        return redirect('/user_index/'+str(d.id))
        
    return render_template("user_contact.html",d=d)



@app.route('/admin_vw_user_feed')
@login_required
def admin_vw_user_feed():
    obj= Contact.query.all()
    return render_template("admin_vw_user_feed.html",obj=obj)






@app.route('/t_confrm_infrm/<id>',methods=['GET', 'POST'])
@login_required
def t_confrm_infrm(id):
    a=Login.query.filter_by(id=current_user.id).first()
    d= Issue.query.filter_by(id=id,cls=a.cls,division=a.division).first()

    if request.method == 'POST':
        uid = request.form['uid']
        tid = request.form['tid']
        subject = request.form['subject']
        issue = request.form['issue']
        uname = request.form['uname']
        uaddress = request.form['uaddress']
        ucontact = request.form['ucontact']
        ucategory = request.form['ucategory']
        ugender = request.form['ugender']
        my_data1 = C_solution(issue_id=id,uid=uid,tid=tid,subject=subject,issue=issue,uname=uname,uaddress=uaddress,ucontact=ucontact,ucategory=ucategory,ugender=ugender)
        db.session.add(my_data1) 
        db.session.commit()
        return redirect('/t_index/'+str(d.id))
    return render_template("t_confrm_infrm.html",d=d)




@app.route('/admin_inform/<int:id>')
@login_required
def admin_inform(id):
    d= C_solution.query.filter_by(id=id).first()
    return render_template("admin_inform.html",d=d)



@app.route('/admin_vw_c/<int:id>')
@login_required
def admin_vw_c(id):
    d= C_solution.query.filter_by(issue_id=id,tid=current_user.id).first()
    obj= Login.query.filter_by(category="counsellor").all()
    
    return render_template("admin_vw_c.html",obj=obj,d=d)



@app.route('/admin_vw_d/<int:id>')
@login_required
def admin_vw_d(id):
    d= C_solution.query.filter_by(issue_id=id,tid=current_user.id).first()
    obj= Login.query.filter_by(category="doctor").all()
    
    return render_template("admin_vw_d.html",obj=obj,d=d)



@app.route('/admin_vw_p/<int:id>')
@login_required
def admin_vw_p(id):
    d= Issue.query.filter_by(id=id,tid=current_user.id).first()
    obj= Login.query.filter_by(category="police").all()
    
    return render_template("admin_vw_p.html",obj=obj,d=d)



@app.route('/t_bk_counslr/<id>/<bid>')
@login_required
def t_bk_counslr(id,bid):
    a= Login.query.filter_by(id=id).first()
    d= C_solution.query.filter_by(id=bid).first()
    d.cid = a.id
    d.cname=a.name
    d.caddress=a.address
    d.ccontact=a.contact
    d.cemail=a.email
    d.coffaddress=a.offaddress
    d.usertype = a.category
    db.session.commit()
    return redirect('/t_index/'+str(current_user.id))
 



