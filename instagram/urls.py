from . import views
from django.urls import path

app_name = "instagram"

urlpatterns = [
    path('post/new/', views.post_new, name = "post_new"),
]
