from dogs_classification import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^dogs_classification$', views.index, name='dogs_classification'),
    url(r'^dogs_classification/poll_state$', views.poll_state, name='dc_poll_state'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
