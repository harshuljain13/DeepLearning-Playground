import views
from django.conf.urls import url


urlpatterns = [
    url(r'^object_detection$', views.index, name='object_detection'),
    url(r'^object_detection/poll_state$', views.poll_state, name='od_poll_state'),
]