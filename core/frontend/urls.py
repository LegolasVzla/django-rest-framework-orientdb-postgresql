from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,CompanyViewSet,OFriendsViewSet,
    OWorksAtViewSet)
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')
router.register('api/company', CompanyViewSet, 'company')
#router.register('api/ousers', OUsersViewSet, 'ousers')
#router.register('api/ocompany', OCompanyViewSet, 'ocompany')
router.register('api/ofriends', OFriendsViewSet, 'ofriends')
router.register('api/oworksat', OWorksAtViewSet, 'oworksat')

schema_view = get_swagger_view(title='Swagger DRF-Orientdb-PostgreSQL REST API Documentation')

urlpatterns = [
    url(r'^swagger/$', schema_view)
]

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)