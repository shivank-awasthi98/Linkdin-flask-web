from application import app
from flask import render_template,request ,json,Response
courseData=[{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"},{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"},{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"},{"courseID":"111","title":"PHP 111","description":"Intro to php","credits":"3","term":"Fall,Spring"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index=True)
@app.route("/login")
def login():
    return render_template("login.html",login=True)
@app.route("/cources/")
@app.route("/cources/<term>")
def cources(term="Spring 2019"):
    
    print(courseData)
    return render_template("cources.html",courseData=courseData,cources=True,term=term)
@app.route("/register")
def register():
    return render_template("register.html",register=True)
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