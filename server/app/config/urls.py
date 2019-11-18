from rest_framework import routers
from summoner.views import SummonerViewSet

router = routers.SimpleRouter()
router.register(prefix='summoners', viewset=SummonerViewSet, base_name="summoner")
urlpatterns = router.urls