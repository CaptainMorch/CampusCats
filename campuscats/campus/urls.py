from .views import CampusViewSet, LocationViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('campuses', CampusViewSet)
router.register('locations', LocationViewSet)

urlpatterns = router.urls
