from django.urls import path
from .views import MarkSpamView

urlpatterns = [
    path('', MarkSpamView.as_view(), name='mark-spam'),
]
