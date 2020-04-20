from django.conf.urls import url
from django.urls import path
from django.views.static import serve

from embeddia.views import EMBEDDIAAnalyzersView


urlpatterns = [
    url(r"^$", EMBEDDIAAnalyzersView.as_view(), name="embeddia"),
]
