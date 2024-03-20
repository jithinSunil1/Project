from django.urls import path
from Admin import views
app_name="webadmin"

urlpatterns = [
        path('ward/',views.ward,name="ward"),
        path('delward/<str:id>',views.delward,name="delward"),
        path('editward/<str:id>',views.editward,name="editward"),
        path('wardmember/',views.wmname,name="wmname"),
        path('location/',views.locname,name="locname"),
        path('dellocation/<str:id>',views.dellocname,name="dellocname"),
        path('editlocation/<str:id>',views.editlocname,name="editlocname"),
        path('category/',views.catname,name="catname"),
        path('delcategory/<str:id>',views.delcatname,name="delcatname"),
        path('editcategory/<str:id>',views.editcatname,name="editcatname"),
        path('mname/',views.mname,name="mname"),
        path('delmname/<str:id>',views.delmname,name="delmname"),
        path('editmname/<str:id>',views.editmname,name="editmname"),
        path('information/',views.Iname,name="Iname"),
        path('delinformation/<str:id>',views.delIname,name="delIname"),
        path('editinformation/<str:id>',views.editIname,name="editIname"),
        path('Viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
        path('Viewfeedback/',views.viewfeedback,name="viewfeedback"),
        path('Admin/',views.admin,name="Admin"),
        path('Homepage/',views.homepage,name="homepage"),
        path('Resources/',views.resources,name="Resources"),
        path('delresources/<str:id>',views.delresources,name="delresources"),
        path("logout/",views.logout,name="logout"),
        
        

       



]