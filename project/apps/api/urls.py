from rest_framework import routers

from .views import (
    ConventionViewSet,
    ContestViewSet,
    GroupViewSet,
    ContestantViewSet,
    DistrictViewSet,
    SongViewSet,
    PersonViewSet,
    SearchViewSet,
)

router = routers.DefaultRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'contests', ContestViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'contestants', ContestantViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'songs', SongViewSet)
router.register(r'searches', SearchViewSet, base_name='search')
urlpatterns = router.urls
