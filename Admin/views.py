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
  "databaseURL" : ""
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
st = firebase.storage()


# Create your views here.
def ward(request):
    Ward=db.collection("tbl_ward").stream()
    ward_data=[]
    for i in Ward:
        data=i.to_dict()
        ward_data.append({"ward":data,"id":i.id})
    if request.method=="POST":
        data={"ward_name":request.POST.get("Wardname")}
        db.collection("tbl_ward").add(data)
        return redirect("webadmin:ward")
    else:
        return render(request,"Admin/ward.html",{"ward":ward_data})
    



def editward(request,id):
    ward=db.collection("tbl_ward").document(id).get().to_dict()
    if request.method=="POST":
       data={"ward_name":request.POST.get("Wardname")}
       db.collection("tbl_ward").document(id).update(data)
       return redirect("webadmin:ward")
    else:
        return render(request,"Admin/ward.html",{"ward_data":ward})

    
def delward(request,id):
    db.collection("tbl_ward").document(id).delete()
    return redirect("webadmin:ward")


def wmname(request):
   Ward=db.collection("tbl_ward").stream()
   ward_data=[]
   for i in Ward:
        data=i.to_dict()
        ward_data.append({"ward":data,"id":i.id})
        result=[] 
   wm=db.collection("tbl_wardmember").stream()
   wm_data=[]
   for wmname in wm_data:
        wm_dict=wm.to_dict()
        ward=db.collection("tbl_ward").document(ward_dict["ward_id"]).get()
        ward_dict=ward.to_dict()
        result.append({'warddata':ward_dict,'wmname_data':wm_dict,'wmnameid':wm.id})
   if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            wardmember = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Wardmember/Userreg.html",{"msg":error})
        image = request.FILES.get("photo")
        if image:
            path = "WardmemberPhoto/" + image.name
            st.child(path).put(image)
            d_url = st.child(path).get_url(None)
        proof = request.FILES.get("proof")
        if proof:
            path = "WardmemberProof/" + proof.name
            st.child(path).put(proof)
            u_url = st.child(path).get_url(None)
        db.collection("tbl_wardmember").add({"wardmember_id":wardmember.uid,"wardmember_name":request.POST.get("wmname"),"wardmember_contact":request.POST.get("contact"),"wardmember_email":request.POST.get("email"),"wardmember_address":request.POST.get("address"),"wardmember_photo":d_url, "wardmember_proof":u_url,"ward_id":request.POST.get("sel_ward")})
        return redirect("webadmin:wmname")  
   else:
    return render(request,"Admin/wardmember.html",{"wm":wm_data,"ward":ward_data})
   


def locname(request):
    loc=db.collection("tbl_Location").stream()
    loc_data=[]
    for i in loc:
        data=i.to_dict()
        loc_data.append({"locname":data,"id":i.id})
    if request.method=="POST":
        data={"location_name":request.POST.get("locname")}
        db.collection("tbl_Location").add(data)
        return redirect("webadmin:locname")
    else:
        return render(request,"Admin/Location.html",{"loc":loc_data})
    

def dellocname(request,id):
    db.collection("tbl_Location").document(id).delete()
    return redirect("webadmin:locname")

def editlocname(request,id):
    loc=db.collection("tbl_Location").document(id).get().to_dict()
    if request.method=="POST":
       data={"location_name":request.POST.get("locname")}
       db.collection("tbl_Location").document(id).update(data)
       return redirect("webadmin:locname")
    else:
        return render(request,"Admin/Location.html",{"loc_data":loc}) 
    

def catname(request):
    cat=db.collection("tbl_category").stream()
    cat_data=[]
    for i in cat:
        data=i.to_dict()
        cat_data.append({"catname":data,"id":i.id})
    if request.method=="POST":
        data={"category_name":request.POST.get("catname")}
        db.collection("tbl_category").add(data)
        return redirect("webadmin:catname")
    else:
        return render(request,"Admin/category.html",{"cat":cat_data})
    
def delcatname(request,id):
     db.collection("tbl_category").document(id).delete()
     return redirect("webadmin:catname")

def editcatname(request,id):
    cat=db.collection("tbl_category").document(id).get().to_dict()
    if request.method=="POST":
       data={"category_name":request.POST.get("catname")}
       db.collection("tbl_category").document(id).update(data)
       return redirect("webadmin:catname")
    else:
        return render(request,"Admin/category.html",{"cat_data":cat}) 
    

    
def mname(request):
    meet=db.collection("tbl_Meeting").stream()
    meet_data=[]
    for i in meet:
        data=i.to_dict()
        meet_data.append({"mname":data,"id":i.id})
    if request.method=="POST":
        data={"meeting_name":request.POST.get("mname"),"meeting_time":request.POST.get("time"),"meeting_date":request.POST.get("date")}
        db.collection("tbl_Meeting").add(data)
        return redirect("webadmin:mname")
    else:
        return render(request,"Admin/Meeting.html",{"meet":meet_data})

def delmname(request,id):
    db.collection("tbl_Meeting").document(id).delete()
    return redirect("webadmin:mname")

def editmname(request,id):
     meet=db.collection("tbl_Meeting").document(id).get().to_dict()
     if request.method=="POST":
        data={"meeting_name":request.POST.get("mname")}
        db.collection("tbl_Meeting").document(id).update(data)
        return redirect("webadmin:mname")
     else:
          return render(request,"Admin/Meeting.html",{"meet_data":meet}) 
     
def Iname(request):
    info=db.collection("tbl_Information").stream()
    info_data=[]
    for i in info:
        data=i.to_dict()
        info_data.append({"Iname":data,"id":i.id})
    if request.method=="POST":
        data={"information_name":request.POST.get("Iname"),"information_description":request.POST.get("dis"),"information_date":request.POST.get("date"),"information_validdate":request.POST.get("vdate")}
        db.collection("tbl_Information").add(data)
        return redirect("webadmin:Iname")
    else:
        return render(request,"Admin/Information.html",{"info":info_data})
    
def delIname(request,id):
    db.collection("tbl_Information").document(id).delete()
    return redirect("webadmin:Iname")

def editIname(request,id):
     info=db.collection("tbl_Information").document(id).get().to_dict()
     if request.method=="POST":
        data={"information_name":request.POST.get("Iname")}
        db.collection("tbl_Information").document(id).update(data)
        return redirect("webadmin:Iname")
     else:
          return render(request,"Admin/Information.html",{"info_data":info}) 


def viewcomplaint(request):
    user_data=[]
    wm_data=[]
    wm = db.collection("tbl_wardmember").stream()
    for w in wm:
        com = db.collection("tbl_complaint").where("wardmember_id", "!=","").where("complaint_status", "==", 0).stream()
    for i in com:
        wm_data.append({"complaint":i.to_dict(),"id":i.id,"wm":w.to_dict()})
    user=db.collection("tbl_userreg").stream()
    for u in user:
         com=db.collection("tbl_complaint").where("user_id","==",u.id).where("complaint_status","==",0).stream()
         for i in com:
            user_data.append({"complaint":i.to_dict(),"id":i.id,"user":u.to_dict()})        
    return render(request,"Admin/ViewComplaint.html",{"wm":wm_data,"user":user_data})    

def viewfeedback(request):
    # user_data=[]
    wm_data=[]
    wm = db.collection("tbl_wardmember").stream()
    for w in wm:
        feed = db.collection("tbl_feedback").stream()
    for i in feed:
        wm_data.append({"feedback":i.to_dict(),"id":i.id,"wm":w.to_dict()})
    # user=db.collection("tbl_userreg").stream()
    # for u in user:
    #      com=db.collection("tbl_complaint").where("user_id","==",u.id).where("complaint_status","==",0).stream()
    #      for i in com:
    #         user_data.append({"complaint":i.to_dict(),"id":i.id,"user":u.to_dict()})        
    return render(request,"Admin/Viewfeedback.html",{"wm":wm_data})    







