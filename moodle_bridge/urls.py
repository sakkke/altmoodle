from django.urls import path
from .views import Sections

urlpatterns = [
    path('sections', Sections.as_view()),
]
