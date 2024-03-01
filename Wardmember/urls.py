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
     path('Reject/',views.Reject,name="Reject"),
      
     
        

]