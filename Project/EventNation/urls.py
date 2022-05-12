from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)

app_name = 'EventNation'
urlpatterns = [
 path("", views.home, name="home"),
 path('createEvent', views.createEvent, name="createEvent"),
 path('register', views.createUser, name="createUser"),
 path('login', views.loginView, name="login"),
 path('logout', views.logoutView, name="logout"),
 path('organizer', views.becomeOrganizer, name="organizer"),
 path('profile', views.profileView, name="profile"),
 path('<int:event_id>/review', views.review, name="review")
]