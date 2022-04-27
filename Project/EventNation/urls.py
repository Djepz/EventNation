from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)

app_name = 'EventNation'
urlpatterns = [
 path("", views.home, name="home"),
 path("", views.criarEvento, name="criarEvento")
]