from django.urls import path
from .views import dashboard,download_excel,image_classification,user_dashboard,dashboard_login,dashboard_logout,image_upload,list_images,dashboard_register


urlpatterns = [
    path("dashboard", dashboard,name="dashboard"),
    path("", user_dashboard,name="home"),
    path("login", dashboard_login,name="login"),
    path("register", dashboard_register,name="register"),
    path("logout", dashboard_logout,name="logout"),
    path("upload", image_upload,name="imageupload"),
    path("listimages", list_images,name="listimages"),
    path("classification", image_classification,name="classification"),
    path('download-excel/', download_excel, name='download_excel'),
]
