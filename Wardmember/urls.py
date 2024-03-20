from django.urls import path
from Wardmember import views
app_name="webwardmember"


urlpatterns = [
     path('complaint/',views.complaint,name="complaint"),
     path('feedback/',views.feedback,name="feedback"),
     path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
     path('delfeedback/<str:id>',views.delfeedback,name="delfeedback"),
     path('viewreq/',views.viewreq,name="viewreq"),
     path('Approve/<str:id>',views.Approve,name="Approve"),
     path('Reject/<str:id>',views.Reject,name="Reject"),
     path('homepage/',views.homepage,name="homepage"),
     path('userreg/',views.userreg,name="userreg"),
     path('Myprofile/',views.Myprofile,name="Myprofile"),
     path('Accept/',views.Accept,name="Accept"),
     path('Rejected/',views.Rejected,name="Rejected"),
     path('changepassword/',views.changepassword,name="changepassword"),
     path('Editprofile/',views.Editprofile,name="Editprofile"),
     path("viewres/",views.viewres,name="viewres"),
     path('view_user/',views.view_user,name="view_user"),
     path('viewresreq/',views.viewresreq,name="viewresreq"),
     path('meeting/',views.mname,name="mname"),
     path('delmname/<str:id>',views.delmname,name="delmname"),
     path('editmname/<str:id>',views.editmname,name="editmname"),
     path('logout/',views.logout,name="logout"),

     
     path('chat/<str:id>',views.chat,name="chat"),
     path('ajaxchat/',views.ajaxchat,name="ajaxchat"),
     path('ajaxchatview/',views.ajaxchatview,name="ajaxchatview"),
     path('clearchat/',views.clearchat,name="clearchat"),  

]