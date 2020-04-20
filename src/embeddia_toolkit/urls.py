from django.conf.urls import url
from django.urls import path
from django.views.static import serve

from embeddia.views import (
    EMBEDDIAAnalyzersView,
    EMBEDDIAGeneratorsView,
    EMBEDDIARootView
)


urlpatterns = [
    url(r"^$", EMBEDDIARootView.as_view(), name="embeddia_root"),
    path("analyzers/", EMBEDDIAAnalyzersView.as_view(), name="embeddia_analyzers"),
    path("generators/", EMBEDDIAGeneratorsView.as_view(), name="embeddia_generators"),     
]
