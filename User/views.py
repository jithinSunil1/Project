from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date

db=firestore.client()
# Create your views here.
def complaint(request):
    com=db.collection("tbl_complaint").stream()
    com_data=[]
    for i in com:
        data=i.to_dict()
        com_data.append({"complaint":data,"id":i.id})
    if request.method=="POST":
        datedata =date.today()
        data={"user_id":request.session["uid"],"complaint_content":request.POST.get("content"),"complaint_date":str(datedata),"complaint_status":0}
        db.collection("tbl_complaint").add(data)
        return redirect("webuser:complaint")
    else:
        return render(request,"User/complaint.html",{"com":com_data})
    

def delcomplaint(request,id):
    db.collection("tbl_complaint").document(id).delete()
    return redirect("webuser:complaint")

    

def feedback(request):
    feed=db.collection("tbl_feedback").stream()
    feed_data=[]
    for i in feed:
        data=i.to_dict()
        feed_data.append({"feedback":data,"id":i.id})
    if request.method=="POST":
        data={"feedback_content":request.POST.get("content"),"feedback_date":request.POST.get("date"),"user_id":request.session["uid"]}
        db.collection("tbl_feedback").add(data)
        return redirect("webuser:feedback")
    else:
        return render(request,"User/feedback.html",{"feed":feed_data})    
     
def delfeedback(request,id):
    db.collection("tbl_feedback").document(id).delete()
    return redirect("webuser:feedback")

def Request(request):
    req=db.collection("tbl_Request").stream()
    req_data=[]
    for i in req:
        data=i.to_dict()
        req_data.append({"Request":data,"id":i.id})
    if request.method=="POST":
        data={"Request_description":request.POST.get("description"),"Request_date":request.POST.get("date")}
        db.collection("tbl_Request").add(data)
        return redirect("webuser:Request")
    else:
        return render(request,"User/Request.html",{"req":req_data})    
    
def homepage(request):
    return render(request,"User/homepage.html")


def sendreq(request):
    wardmem = ""
    cat=db.collection("tbl_category").stream()
    cat_data=[]
    for i in cat:
        data=i.to_dict()
        cat_data.append({"cat":data,"id":i.id})
    result=[]
    send_data=db.collection("tbl_sendreq").stream()
    for i in send_data:
        data=i.to_dict()
        wardmember=db.collection("tbl_wardmember").document(data["wardmember_id"]).get().to_dict()
        result.append({"send":data,"id":i.id,"wardmember":wardmember,"cat":cat})
    if request.method=="POST":
        
        user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
        wardid = user["ward_id"]
        wardmember = db.collection("tbl_wardmember").where("ward_id", "==", wardid).stream()
        wardmem = ""
        for wm in wardmember:
            wardmem = wm.id
        datedata = date.today()
        data={"sendreq_category":request.POST.get("category"),"sendreq_description":request.POST.get("descrip"),"request_date":str(datedata),"wardmember_id":wardmem,"user_id":request.session["uid"],"viewstatus":0}
        db.collection("tbl_sendreq").add(data)
        return redirect("webuser:sendreq")
    else:
        return render(request,"User/sendreq.html",{"cat":cat_data,"send":result})    



def Myprofile(request):
    if 'uid' in request.session:
        user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
        # print(user["user_photo"])
        return render(request,"User/Myprofile.html",{'user':user})
    else:
        return redirect("webguest:login")


def Editprofile(request):
    if 'uid' in request.session:
        data = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
        if request.method == "POST":
            data = {'user_name':request.POST.get('txt_name'),'user_contact':request.POST.get('txt_contact'),'user_address':request.POST.get('txt_address')}
            db.collection("tbl_user").document(request.session["uid"]).update(data)
            return redirect("webuser:Myprofile")
        else:
            return render(request,"User/EditProfile.html",{'user':data})
    else:
        return redirect("webguest:login")



def changepassword(request):
  user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
  email = user["user_email"]
  password_link = firebase_admin.auth.generate_password_reset_link(email) 
  send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET user.",#body
    settings.EMAIL_HOST_USER,
    [email],
  )
  return render(request,"User/Homepage.html",{"msg":email})

