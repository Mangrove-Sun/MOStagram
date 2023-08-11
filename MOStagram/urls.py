from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', login_required(TemplateView.as_view(template_name = 'root.html')), name = 'root'),
    # re_path('', TemplateView.as_view(template_name = 'root.html'), name = 'root') # 보통 404구현할 때 쓰이기도 함.
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)