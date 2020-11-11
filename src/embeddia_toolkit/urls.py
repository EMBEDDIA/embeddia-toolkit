from django.urls import include, path
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='api/v1/', permanent=False), name='index'),
    path('api/v1/', include(('embeddia_toolkit.urls_v1', 'embeddia_v1'), namespace='v1')),
]
