from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)

app_name = 'EventNation'
urlpatterns = [
 path("", views.home, name="home"),
 path('createEvent', views.createEvent, name="createEvent"),
 path('register', views.createUser, name="CreateUser"),
 path('login', views.loginView, name="login"),
 path('logout', views.logoutView, name="logout"),
 path('profile', views.profileView, name="profile"),
 path('about', views.about, name="about"),
 path('TopRated', views.TopRated, name="TopRated"),
 path('<int:event_id>/review', views.review, name="review"),
 path('<int:event_id>/comment', views.comment, name="comment"),
 path('<int:event_id>', views.eventPage, name="eventPage"),
 path('<category>', views.categoryPage, name="category"),
 path('<int:event_id>/purchase', views.purchase, name="purchase"),
 path('<int:event_id>/AlterEvent', views.alterEvent, name="alterEvent"),
 path('<int:event_id>/RemoveEvent', views.removeEvent, name="removeEvent")
]
