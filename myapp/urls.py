from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact',views.contact,name="contact"),
    path('findbus', views.findbus, name="findbus"),
    path('bookings/<int:bus_id>/', views.bookings, name="bookings"),
    path('cancellings/<int:book_id>/', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),
    path('ticket/<int:id>/',views.ticket,name="ticket"),
    path('ticket/download/<int:id>/',views.downloadPDF,name="download ticket"),

]
