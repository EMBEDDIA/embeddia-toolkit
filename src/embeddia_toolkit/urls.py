from django.conf.urls import url
from django.urls import path
from django.views.static import serve

from embeddia.views import (
    EMBEDDIAArticleAnalyzerView,
    EMBEDDIACommentAnalyzerView,
    EMBEDDIAGeneratorsView,
    EMBEDDIARootView,
    EMBEDDIAHealthView
)


urlpatterns = [
    url(r"^$", EMBEDDIARootView.as_view(), name="embeddia_root"),
    path("article_analyzer/", EMBEDDIAArticleAnalyzerView.as_view(), name="embeddia_article_analyzer"),
    path("comment_analyzer/", EMBEDDIACommentAnalyzerView.as_view(), name="embeddia_comment_analyzer"),
    path("article_generator/", EMBEDDIAGeneratorsView.as_view(), name="article_generator"),
    #path("dashboard/", EMBEDDIADashboardView.as_view(), name="embeddia_dashboard"),
    path("health/", EMBEDDIAHealthView.as_view(), name="embeddia_health"),  
]
