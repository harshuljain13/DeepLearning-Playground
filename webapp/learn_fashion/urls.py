from django.conf.urls import url
import views

urlpatterns = [
    url(r'^learn_fashion$', views.index, name='learn_fashion'),
]