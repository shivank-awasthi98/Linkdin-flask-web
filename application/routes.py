from application import app,db
from flask import render_template,request ,json,Response,flash,redirect,url_for
from application.models import User,Course,Enrollment
from application.forms import LoginForm,RegisterForm

courseData=[{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"},{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"},{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"},{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index=True)



@app.route("/login",methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        

        user = User.objects(email=email).first()
       
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in","success")
            return redirect("/index")

        else:
            flash("Sorry somthing went wrong",'danger')
    return render_template("login.html",title='Login',form=form,login=True)



@app.route("/cources/")
@app.route("/cources/<term>")
def cources(term="Spring 2019"):
    
    print(courseData)
    return render_template("cources.html",courseData=courseData,cources=True,term=term)



@app.route("/register",methods=['POST','GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id    += 1
        # print(form)

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data


        user        = User(user_id=user_id,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    
    return render_template("register.html",title='Register',form=form,register=True)

    



@app.route("/enrolment",methods=["GET","POST"])
def enrolment():
    id=request.form.get('courseID')
    title=request.form.get('title')
    term=request.form.get('term')
    
    return render_template("enrolment.html",register=True,data={"id":id,"term":term,"title":title})    



@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx==None):
        jdata=courseData
    else:
        jdata=courseData[int(idx)]
    return Response(json.dumps(jdata),mimetype="application/json")





@app.route("/user")
def user():
    # User(user_id  =  1,
    #     first_name  =  'christian',
    #     last_name  =  'Hur',
    #     email  =  'christHur@uta.com',
    #     password = 'aaa12@@@').save()
    # User(user_id  =  2,
    #     first_name  =  'christopher',
    #     last_name  =  'Hur',
    #     email  =  'christHur@uta.com',
    #     password = 'aaa12@@@').save()
    users=User.objects.all()
    return render_template('user.html',users=users)
    

