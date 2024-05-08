from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from secretary.views import LandingPageView, ProfileView
from users.views import LoginView, LogoutView
from secretary.views import ExportCSVView




urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', LandingPageView.as_view(), name="landing-page"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('item/', include('secretary.urls', namespace='secretary')),
    path('user/', include('users.urls', namespace='users')),
    path('room/', include('rooms.urls', namespace='rooms')),
    path('staffs/', include('staffs.urls', namespace='staffs')),
    path('equipment/', include('rlab.urls', namespace='equipments')),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('export-csv/', ExportCSVView.as_view(), name='export-csv'),
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)