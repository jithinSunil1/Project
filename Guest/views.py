from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase

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
# Create

def Login(request): 
    userid = ""
    wmnameid =""
    adminid=""

    if request.method=="POST":
        email = request.POST.get("email")  
        password =request.POST.get("password")
        try:
            data = authe.sign_in_with_email_and_password(email,password) 
        except:
            return render(request,"Guest/Login.html",{"msg":"Error in Email or password"})
        user=db.collection("tbl_user").where("user_id","==",data["localId"]).stream()
        for u in user:
            userid=u.id
        wmname=db.collection("tbl_wardmember").where("wardmember_id","==",data["localId"]).stream()
        for i in wmname:
            wmnameid=i.id
        admin=db.collection("tbl_admin").where("admin_id","==",data["localId"]).stream()
        for i in admin:
            adminid=i.id    
        if userid:
            request.session["uid"]= userid
            return redirect("webuser:homepage")
        elif wmnameid:
            request.session["wmid"]= wmnameid
            return redirect("webwardmember:homepage")
        elif adminid:
            request.session["aid"]=adminid
            return redirect("webadmin:homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"error"})    
    else:
        return render(request,"Guest/Login.html")

    

