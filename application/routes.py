from application import app,db
from flask import render_template,request ,json,Response,flash,redirect,url_for,session
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
    if session.get('username'):
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        

        user = User.objects(email=email).first()
       
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in","success")
            session['user_id']   = user.user_id
            session['username']  = user.first_name
            return redirect("/index")

        else:
            flash("Sorry somthing went wrong",'danger')
    return render_template("login.html",title='Login',form=form,login=True)



@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))


@app.route("/cources/")
@app.route("/cources/<term>")
def cources(term=None):
    if term is None:
        term = "Spring 2019"
    classes = Course.objects.order_by("courseID") #'+' or '-' for accending or decending *default '+'

    
    
    return render_template("cources.html",courseData=classes,cources=True,term=term)



@app.route("/register",methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
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

    



@app.route("/enrollment",methods=["GET","POST"])
def enrollment():
    print("c1")
    if not session.get('username'):
        return redirect(url_for('login'))
    courseID    = request.form.get('courseID')
    courseTitle  = request.form.get('courseTitle')

    user_id = session.get('user_id')
    classes=list( User.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'enrollment', 
                        'localField': 'user_id', 
                        'foreignField': 'user_id', 
                        'as': 'r1'
                    }
                }, {
                    '$unwind': {
                        'path': '$r1', 
                        'includeArrayIndex': 'r1_id', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$lookup': {
                        'from': 'course', 
                        'localField': 'r1.courseID', 
                        'foreignField': 'courseID', 
                        'as': 'r2'
                    }
                }, {
                    '$unwind': {
                        'path': '$r2', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'user_id': user_id
                    }
                }, {
                    '$sort': {
                        'courseID': 1
                    }
                }
            ]) )


    if courseID:
        print("c4")
        if Enrollment.objects(user_id= user_id,courseID=courseID):
            print("c2")
            flash(f"Oops You are already registered in this course {courseTitle}!","danger")
            return redirect(url_for("cources"))
        else:
            print("c3")
            Enrollment(user_id= user_id,courseID= courseID).save()
            flash(f"You are enrolled in {courseTitle}","success")
        
    term=request.form.get('term')
    
    return render_template("enrollment.html",enrollment=True,title="Enrollment",classes=classes)    



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
    

