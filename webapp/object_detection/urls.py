from django.conf.urls import url
import views

urlpatterns = [
    url(r'^object_detection$', views.index, name='object_detection'),
]