from django.urls import path
from User import views
app_name="webuser"


urlpatterns = [
     path('complaint/',views.complaint,name="complaint"),
     path('feedback/',views.feedback,name="feedback"),
     path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
     path('delfeedback/<str:id>',views.delfeedback,name="delfeedback"),
     path('Request/<str:id>',views.Request,name="Request"),
     path('homepage/',views.homepage,name="homepage"),
     path('sendreq/',views.sendreq,name="sendreq"),
     path('Myprofile/',views.Myprofile,name="Myprofile"),
     path("Editprofile/",views.Editprofile,name="Editprofile"),
     path("changepassword/",views.changepassword,name="changepassword"),
     path("viewres/",views.viewres,name="viewres"),
     path("logout/",views.logout,name="logout"),
     path("myresreq/",views.myresreq,name="myresreq"),
     path("approveresreq/",views.approveresreq,name="approveresreq"),


     path('chat/<str:id>',views.chat,name="chat"),
     path('ajaxchat/',views.ajaxchat,name="ajaxchat"),
     path('ajaxchatview/',views.ajaxchatview,name="ajaxchatview"),
     path('clearchat/',views.clearchat,name="clearchat"),    
]