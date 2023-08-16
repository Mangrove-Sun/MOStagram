from django.urls import path, re_path
from . import views

app_name = "instagram"

urlpatterns = [
  path('', views.index, name = 'index'),
  path('post/new/', views.post_new, name = "post_new"),
  path('post/<int:pk>/', views.post_detail, name = "post_detail"),
  path('post/<int:pk>/like/', views.post_like, name = "post_like"),
  path('post/<int:pk>/unlike/', views.post_unlike, name = "post_unlike"),
  # re_path에서 정규표현식 사용시 시작(')과 끝(') 사이에 $가 반드시 있어야 한다.
  # 그렇지 않으면 정의한 정규표현식 패턴대로 끝나지 않아도 항상 정의한 패턴에 포함이 된다.
  re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_page, name = "user_page"),
]
