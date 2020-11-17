from django.conf.urls import url
from django.urls import path
from django.views.static import serve

from embeddia_toolkit.embeddia.views import (
    EMBEDDIAArticleAnalyzerView,
    EMBEDDIACommentAnalyzerView,
    EMBEDDIARootView,
    EMBEDDIAHealthView
)

urlpatterns = [
    url(r"^$", EMBEDDIARootView.as_view(), name="embeddia_root"),
    path("article_analyzer/", EMBEDDIAArticleAnalyzerView.as_view(), name="embeddia_article_analyzer"),
    path("comment_analyzer/", EMBEDDIACommentAnalyzerView.as_view(), name="embeddia_comment_analyzer"),
    path("health/", EMBEDDIAHealthView.as_view(), name="embeddia_health"),  
]
