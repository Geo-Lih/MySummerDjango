from django.urls import include, path

urlpatterns = [

    path('eshop/', include('apps.eshop.urls')),
    path('blog/', include('apps.blog.urls')),
    path('user/', include('apps.user.urls')),
    path('', include('apps.home.urls')),
]
