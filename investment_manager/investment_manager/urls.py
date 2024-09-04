from django.contrib import admin
from django.urls import path, include
from funds.views import Login, Refresh

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fund/', include('funds.urls')),
    path('token/', Login.as_view(), name='token_obtain_pair'),
    path('token/refresh/', Refresh.as_view(), name='token_refresh'),
]