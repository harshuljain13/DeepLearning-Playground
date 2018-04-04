import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^ocr_classification$', views.index, name='ocr_classification'),
    url(r'^ocr_classification/poll_state$', views.poll_state, name='ocr_poll_state'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
