from django.conf.urls import url
from django.urls import path
from django.views.static import serve

from embeddia.views import EMBEDDIATextView


urlpatterns = [
    path("embeddia", EMBEDDIATextView.as_view(), name="embeddia"),
]
