from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import include, url
#from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet)

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')

urlpatterns = router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
