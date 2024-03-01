from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from datetime import date

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
    

def delcomplaint(request,id):
    db.collection("tbl_complaint").document(id).delete()
    return redirect("webwardmember:complaint")




    

def feedback(request):
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
    

def delfeedback(request,id):
    db.collection("tbl_feedback").document(id).delete()
    return redirect("webwardmember:feedback")

def viewreq(request):
    vreq = db.collection("tbl_sendreq").where("viewstatus","==",0).stream()
    vreq_data = []
    for i in vreq:
        c = i.to_dict()
        cat = db.collection("tbl_category").document(c["sendreq_category"]).get().to_dict()
        user = db.collection("tbl_user").document(c["user_id"]).get().to_dict()
        vreq_data.append({"sendreq":i.to_dict(),"id":i.id,"cat":cat,"user":user})
    return render(request,"Wardmember/Viewreq.html",{"viewreq":vreq_data})

def Approve(request,id):
    db.collection("tbl_sendreq").document(id).update({"viewstatus":1})
    return redirect("webwardmember:viewreq")

def Reject(request,id):
    db.collection("tbl_sendreq").document(id).update({"viewstatus":2})
    return redirect("webwardmember:viewreq")


def Myprofile(request):
    wm = db.collection("tbl_Wardmember").document(request.session["wmid"]).get().to_dict()
    return render(request,"Wardmember/Myprofile.html",{'wardmember':wm})
    
def Accept(request):
    vreq = db.collection("tbl_sendreq").where("viewstatus","==",1).stream()
    vreq_data = []
    for i in vreq:
        c = i.to_dict()
        cat = db.collection("tbl_category").document(c["sendreq_category"]).get().to_dict()
        user = db.collection("tbl_user").document(c["user_id"]).get().to_dict()
        vreq_data.append({"sendreq":i.to_dict(),"id":i.id,"cat":cat,"user":user})
    return render(request,"Wardmember/AcceptReq.html",{"viewreq":vreq_data})

def Reject(request):
    vreq = db.collection("tbl_sendreq").where("viewstatus","==",2).stream()
    vreq_data = []
    for i in vreq:
        c = i.to_dict()
        cat = db.collection("tbl_category").document(c["sendreq_category"]).get().to_dict()
        user = db.collection("tbl_user").document(c["user_id"]).get().to_dict()
        vreq_data.append({"sendreq":i.to_dict(),"id":i.id,"cat":cat,"user":user})
    return render(request,"Wardmember/RejectReq.html",{"viewreq":vreq_data})




def homepage(request):
    return render(request,"Wardmember/homepage.html")

def userreg(request):
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
    


    