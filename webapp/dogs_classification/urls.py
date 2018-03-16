import views
from django.conf.urls import url


urlpatterns = [
    url(r'^dogs_classification$', views.index, name='dogs_classification'),
    url(r'^dogs_classification/poll_state$', views.poll_state, name='dc_poll_state'),
]