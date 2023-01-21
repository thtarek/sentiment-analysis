from django.urls import path, include
from .views import *

urlpatterns = [
       path('comment/', EnterComment.as_view(), name='comment'),
]