from django.urls import path
from User import views
app_name="webuser"


urlpatterns = [
     path('complaint/',views.complaint,name="complaint"),
     path('feedback/',views.feedback,name="feedback"),
     path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
     path('delFeedback/<str:id>',views.delFeedback,name="delFeedback"),
     path('Request/',views.Request,name="Request"),
     path('homepage/',views.homepage,name="homepage"),
     path('sendreq/',views.sendreq,name="sendreq"),
     path('Myprofile/',views.Myprofile,name="Myprofile"),
     path("Editprofile/",views.Editprofile,name="Editprofile"),
 
]