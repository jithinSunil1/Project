from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime

db=firestore.client()

config = {
    
  "apiKey": "AIzaSyAa89lnPkcx5JrfJopugOa0YAwNe647nUk",
  "authDomain": "lakshya-ac3d9.firebaseapp.com",
  "projectId": "lakshya-ac3d9",
  "storageBucket": "lakshya-ac3d9.appspot.com",
  "messagingSenderId": "714784057945",
  "appId": "1:714784057945:web:9b1861e9910d212064df48",
  "measurementId": "G-ZHJJBS7TFP",
  "databaseURL" :""
}


firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
st = firebase.storage()
# Create your views here.
def complaint(request):
    if 'Wmid' in request.session:    
        com=db.collection("tbl_complaint").stream()
        com_data=[]
        for i in com:
            data=i.to_dict()
            com_data.append({"complaint":data,"id":i.id})
        if request.method=="POST":
            datedata =date.today()
            data={"wardmember_id":request.session["wmid"],"complaint_content":request.POST.get("content"),"complaint_date":str(datedata),"complaint_status":0}
            db.collection("tbl_complaint").add(data)
            return redirect("webwardmember:complaint")
        else:
            return render(request,"Wardmember/complaint.html",{"com":com_data})
    else:
        return render(request,"Guest/Login.html") 

def delcomplaint(request,id):
    db.collection("tbl_complaint").document(id).delete()
    return redirect("webwardmember:complaint")




    

def feedback(request):
    if 'Wmid' in request.session:
        feed=db.collection("tbl_feedback").stream()
        feed_data=[]
        for i in feed:
            data=i.to_dict()
            feed_data.append({"feedback":data,"id":i.id})
        if request.method=="POST":
            data={"feedback_content":request.POST.get("content"),"feedback_date":request.POST.get("date"),"wardmember_id":request.session["wmid"]}
            db.collection("tbl_feedback").add(data)
            return redirect("webwardmember:feedback")
        else:
            return render(request,"Wardmember/feedback.html",{"feed":feed_data})
    else:
        return render(request,"Guest/Login.html")    
    

def delfeedback(request,id):
    db.collection("tbl_feedback").document(id).delete()
    return redirect("webwardmember:feedback")

def viewreq(request):
    if 'wmid' in request.session:
        vreq = db.collection("tbl_sendreq").where("viewstatus","==",0).stream()
        vreq_data = []
        for i in vreq:
            c = i.to_dict()
            cat = db.collection("tbl_category").document(c["sendreq_category"]).get().to_dict()
            user = db.collection("tbl_user").document(c["user_id"]).get().to_dict()
            vreq_data.append({"sendreq":i.to_dict(),"id":i.id,"cat":cat,"user":user})
            return render(request,"Wardmember/Viewreq.html",{"viewreq":vreq_data})
        else:
            return render(request,"Guest/Login.html")
    
     

def Approve(request,id):
    
    db.collection("tbl_sendreq").document(id).update({"viewstatus":1})
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    email = user["user_email"]
    send_mail(
    'REPLY FOR UR REQUEST ', 
    "\rHello \r\nYour request has been accepted",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Wardmember/Homepage.html",{"msg":email})
    

def Reject(request,id):
    
    db.collection("tbl_sendreq").document(id).update({"viewstatus":2})
    
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    email = user["user_email"]
    send_mail(
    'REPLY FOR UR REQUEST ', 
    "\rHello \r\nYour request has been accepted",#body
    settings.EMAIL_HOST_USER,
    [email],
    )
    return render(request,"Wardmember/Homepage.html",{"msg":email})


def Myprofile(request):
    if 'Wmid' in request.session:
        wm = db.collection("tbl_wardmember").document(request.session["wmid"]).get().to_dict()
        return render(request,"Wardmember/Myprofile.html",{'wm':wm})
    else:
        return render(request,"Guest/Login.html")

def Editprofile(request):
    if 'Wmid' in request.session:
        wm = db.collection("tbl_wardmember").document(request.session["wmid"]).get().to_dict()
        if request.method=="POST":
            data={"wardmember_name":request.POST.get("name"),"wardmember_contact":request.POST.get("contact"),"wardmember_address":request.POST.get("address")}
            db.collection("tbl_wardmember").document(request.session["wmid"]).update(data)
            return redirect("webwardmember:Myprofile")
        else:
            return render(request,"Wardmember/EditProfile.html",{"wm":wm}) 
    else:
        return render(request,"Guest/Login.html")     

def changepassword(request):
    if 'Wmid' in request.session:
        wm = db.collection("tbl_wardmember").document(request.session["wmid"]).get().to_dict()
        email = wm["wardmember_email"]
        password_link = firebase_admin.auth.generate_password_reset_link(email) 
    send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET user.",#body
    settings.EMAIL_HOST_USER,
    [email],
  )
    return render(request,"Wardmember/Homepage.html",{"msg":email})




def viewres(request):
  if 'Wmid' in request.session:
    res=db.collection("tbl_Resources").stream()
    res_data=[]
    for i in res:
      data=i.to_dict()
      res_data.append({"res":data,"id":i.id,})
  
    return render(request,"Wardmember/viewres.html",{"res":res_data})
  else:
        return render(request,"Guest/Login.html")    



def Accept(request):
    if 'Wmid' in request.session:
       vreq = db.collection("tbl_sendreq").where("viewstatus","==",1).stream()
       vreq_data = []
    for i in vreq:
        c = i.to_dict()
        cat = db.collection("tbl_category").document(c["sendreq_category"]).get().to_dict()
        user = db.collection("tbl_user").document(c["user_id"]).get().to_dict()
        vreq_data.append({"sendreq":i.to_dict(),"id":i.id,"cat":cat,"user":user})
    return render(request,"Wardmember/AcceptReq.html",{"viewreq":vreq_data})

def Rejected(request):
    if 'Wmid' in request.session:
        vreq = db.collection("tbl_sendreq").where("viewstatus","==",2).stream()
        vreq_data = []
        for i in vreq:
          c = i.to_dict()
          cat = db.collection("tbl_category").document(c["sendreq_category"]).get().to_dict()
          user = db.collection("tbl_user").document(c["user_id"]).get().to_dict()
          vreq_data.append({"sendreq":i.to_dict(),"id":i.id,"cat":cat,"user":user})
          return render(request,"Wardmember/RejectReq.html",{"viewreq":vreq_data})
    else:
        return render(request,"Guest/Login.html")

def viewresreq(request):
    if 'Wmid' in request.session:
       resq=db.collection("tbl_Resources").stream()
       resq_data=[]
       for i in resq:
            data=i.to_dict()
            user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()
            resq_data.append({"resq":data,"id":i.id,"user":user})
            return render(request,"Wardmember/viewresreq.html",{"resq":resq_data}) 
    else:
        return render(request,"Guest/Login.html")   




def homepage(request):
    info=db.collection("tbl_Information").stream()
    info_data=[]
    for i in info:
        data=i.to_dict()
        info_data.append({"Iname":data,"id":i.id})
    return render(request,"Wardmember/homepage.html",{"info":info_data})




def mname(request):
    meet=db.collection("tbl_Meeting").where("Wardmember_id","==",request.session["wmid"]).stream()
    meet_data=[]
    for i in meet:
        data=i.to_dict()
        meet_data.append({"mname":data,"id":i.id})    
    if request.method=="POST":
        wardmem = db.collection("tbl_wardmember").document(request.session["wmid"]).get().to_dict()
        ward = wardmem["ward_id"]
        user = db.collection("tbl_user").where("ward_id", "==", ward).stream()
        for u in user:
           us = u.to_dict()
        #    print(us["user_email"])
           send_mail(
            'MEETING SCHEDULED ', 
            "\rHello \r\nYour meeting has been schedule",#body
            settings.EMAIL_HOST_USER,
            [us["user_email"]],
            ) 
        data={"Wardmember_id":request.session["wmid"],"meeting_name":request.POST.get("mname"),"meeting_time":request.POST.get("time"),"meeting_date":request.POST.get("date")}
        db.collection("tbl_Meeting").add(data)
        return redirect("webwardmember:mname")
    else:
        return render(request,"Wardmember/Meeting.html",{"meet":meet_data})
    
def delmname(request,id):
    db.collection("tbl_Meeting").document(id).delete()
    return redirect("webwardmember:mname")

def editmname(request,id):
     meet=db.collection("tbl_Meeting").document(id).get().to_dict()
     if request.method=="POST":
        data={"meeting_name":request.POST.get("mname")}
        db.collection("tbl_Meeting").document(id).update(data)
        return redirect("webwardmember:mname")
     else:
          return render(request,"Wardmember/Meeting.html",{"meet_data":meet}) 



def userreg(request):
    if 'Wmid' in request.session:
      ward= db.collection("tbl_ward").stream()
      ward_data = []
      for i in ward:
        ward_data.append({"ward":i.to_dict(),"id":i.id})
        if request.method =="POST":
          email = request.POST.get("email")
          password = request.POST.get("password")
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Wardmember/Userreg.html",{"msg":error})
        image = request.FILES.get("photo")
        if image:
              path = "UserPhoto/" + image.name
              st.child(path).put(image)
              d_url = st.child(path).get_url(None)

        proof = request.FILES.get("proof")
        if proof:
            path = "UserProof/" + proof.name
            st.child(path).put(proof)
            k_url = st.child(path).get_url(None)
       
            

            db.collection("tbl_user").add({"user_id":user.uid,"user_name":request.POST.get("uname"),"user_contact":request.POST.get("contact"),"user_email":request.POST.get("email"),"user_address":request.POST.get("address"),"ward_id":request.POST.get("sel_ward"),"user_photo":d_url,"user_proof":k_url})
            return render(request,"Wardmember/Userreg.html")
        else:
            return render(request,"Wardmember/Userreg.html",{"ward":ward_data})
    else:
        return render(request,"Guest/Login.html")
    
def view_user(request):
        if 'Wmid' in request.sesson:
            wardmem = db.collection("tbl_wardmember").document(request.session["wmid"]).get().to_dict()
            ward = wardmem["ward_id"]
            user = db.collection("tbl_user").where('ward_id', '==', ward).stream()
            userd = []
            for i in user:
             userd.append({"user":i.to_dict(),"id":i.id})
            return render(request,"Wardmember/View_user.html",{"user":userd})
        else:
            return render(request,"Guest/Login.html")

##################################################################################################################

def chat(request,id):
    to_user = db.collection("tbl_user").document(id).get().to_dict()
    return render(request,"Wardmember/Chat.html",{"user":to_user,"tid":id})

def ajaxchat(request):
    image = request.FILES.get("file")
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        st.child(path).put(image)
        d_url = st.child(path).get_url(None)
        db.collection("tbl_chat").add({"chat_content":"","chat_time":datetime.now(),"member_from":request.session["wmid"],"user_to":request.POST.get("tid"),"chat_file":d_url,"member_to":"","user_from":""})
        return render(request,"Wardmember/Chat.html",{"tid":tid})
    else:
        if request.POST.get("msg")!="":
            
            db.collection("tbl_chat").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"member_from":request.session["wmid"],"user_to":request.POST.get("tid"),"chat_file":"","member_to":"","user_from":""})
        return render(request,"Wardmember/Chat.html",{"tid":tid})

def ajaxchatview(request):
    tid = request.GET.get("tid")
    chat = db.collection("tbl_chat").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["member_from"] == request.session["wmid"]) | (cdata["member_to"] == request.session["wmid"])) & ((cdata["user_from"] == tid) | (cdata["user_to"] == tid)):
            data.append(cdata)
    return render(request,"Wardmember/ChatView.html",{"data":data,"tid":tid})

def clearchat(request):
    toid = request.GET.get("tid")
    chat_data1 = db.collection("tbl_chat").where("member_from", "==", request.session["wmid"]).where("user_to", "==", request.GET.get("tid")).stream()
    for i1 in chat_data1:
        i1.reference.delete()
    chat_data2 = db.collection("tbl_chat").where("member_to", "==", request.session["wmid"]).where("user_from", "==", request.GET.get("tid")).stream()
    for i2 in chat_data2:
        i2.reference.delete()
    return render(request,"Wardmember/ClearChat.html",{"msg":"Chat Cleared Sucessfully....."})


def logout(request):
    del request.session["wmid"]
    return redirect("webguest:Login")   
