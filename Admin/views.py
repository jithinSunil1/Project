from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from datetime import date,datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

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
    if 'aid' in request.session:    
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
    else:
            return render(request,"Guest/Login.html")    



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
   if 'aid' in request.session:
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
                wmcount = db.collection("tbl_wardmember").where("ward_id", "==", request.POST.get("sel_ward")).stream()
                count = 0
                for wmc in wmcount:
                    count = count + 1
                if count == 0:       
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
                    
                    send_mail(
                        'Account Details ', #subject
                        "\rHello \r\nFollow is ur email " + email + "\n"  +".\n this is ur password"+password,#body
                        settings.EMAIL_HOST_USER,
                        [email],
                    )   
                    db.collection("tbl_wardmember").add({"wardmember_id":wardmember.uid,"wardmember_name":request.POST.get("wmname"),"wardmember_contact":request.POST.get("contact"),"wardmember_email":request.POST.get("email"),"wardmember_address":request.POST.get("address"),"wardmember_photo":d_url, "wardmember_proof":u_url,"ward_id":request.POST.get("sel_ward")})
                    return redirect("webadmin:wmname")  
                else:
                    return render(request,"Admin/wardmember.html",{"msg":"Ward Member Already registred for this ward.."})
        else:
            return render(request,"Admin/wardmember.html",{"wm":wm_data,"ward":ward_data})
        
   else:
            return render(request,"Guest/Login.html")    


def locname(request):
    if 'aid' in request.session:
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
    else:
            return render(request,"Guest/Login.html")    
    

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
    if 'aid' in request.session:
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
    else:
            return render(request,"Guest/Login.html")    

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
    if 'aid' in request.session:
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
    else:
            return render(request,"Guest/Login.html")    

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
    if 'aid' in request.session:
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
    else:
            return render(request,"Guest/Login.html")    
    
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
    if 'aid' in request.session:
    
        user_data=[]
        wm_data=[]
        wcom = db.collection("tbl_complaint").where("wardmember_id", "!=",0).where("complaint_status", "==", 0).stream()
        for i in wcom:
            wdata = i.to_dict()
            wm = db.collection("tbl_wardmember").document(wdata["wardmember_id"]).get().to_dict()
            wm_data.append({"complaint":i.to_dict(),"id":i.id,"wm":wm})

        ucom=db.collection("tbl_complaint").where("user_id","!=",0).where("complaint_status","==",0).stream()
        for i in ucom:
            udata = i.to_dict()
            user = db.collection("tbl_user").document(udata["user_id"]).get().to_dict()
            user_data.append({"complaint":i.to_dict(),"id":i.id,"user":user})  
        return render(request,"Admin/ViewComplaint.html",{"wm":wm_data,"user":user_data})    
    else:
            return render(request,"Guest/Login.html")    


def viewfeedback(request):
    if 'aid' in request.session:
    
        user_data=[]
        wm_data=[]
        wfeed = db.collection("tbl_feedback").where("wardmember_id", "!=",0).stream()
        for i in wfeed:
            wdata = i.to_dict()
            wm = db.collection("tbl_wardmember").document(wdata["wardmember_id"]).get().to_dict()
            wm_data.append({"feedback":i.to_dict(),"id":i.id,"wm":wm})

        ufeed=db.collection("tbl_feedback").where("user_id","!=",0).stream()
        for i in ufeed:
            udata = i.to_dict()
            user = db.collection("tbl_user").document(udata["user_id"]).get().to_dict()
            user_data.append({"feedback":i.to_dict(),"id":i.id,"user":user})  
        return render(request,"Admin/Viewfeedback.html",{"wm":wm_data,"user":user_data})    
    else:
            return render(request,"Guest/Login.html")    


def admin(request):
    if 'aid' in request.session:
        if request.method =="POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                admin = firebase_admin.auth.create_user(email=email,password=password)
            except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
                return render(request,"Admin/Admin.html",{"msg":error})
            db.collection("tbl_admin").add({"admin_id":admin.uid,"admin_name":request.POST.get("name"),"admin_contact":request.POST.get("contact"),"admin_email":request.POST.get("email")})    
            return render(request,"Admin/Admin.html")
        else:
            return render(request,"Admin/Admin.html")
    else:
            return render(request,"Guest/Login.html")    
    

def homepage(request):
    if 'aid' in request.session:
        info=db.collection("tbl_Information").stream()
        info_data=[]
        for i in info:
            data=i.to_dict()
            info_data.append({"Iname":data,"id":i.id})
        # print(info_data)    
        return render(request,"Admin/Homepage.html",{"info":info_data})
    else:
            return render(request,"Guest/Login.html")    


def resources(request):
    if 'aid' in request.session:
        res=db.collection("tbl_Resources").stream()
        res_data=[]
        for i in res:
            data=i.to_dict()
            res_data.append({"res":data,"id":i.id})
        if request.method=="POST":
            datedata =date.today()
            data={"project_name":request.POST.get("name"),"Description":request.POST.get("dis"),"project_date":str(datedata)}
            db.collection("tbl_Resources").add(data)
            return redirect("webadmin:Resources")
        else:
            return render(request,"Admin/Resources.html",{"res":res_data})
    else:
            return render(request,"Guest/Login.html")    


def delresources(request,id):
    db.collection("tbl_Resources").document(id).delete()
    return redirect("webadmin:Resources")


def logout(request):
    del request.session["aid"]
    return redirect("webguest:Login")   


