from rest_framework import routers
from match.views import MatchViewSet
from summoner.views import SummonerViewSet

router = routers.SimpleRouter()
router.register(prefix='summoners', viewset=SummonerViewSet, base_name="summoner")
router.register(prefix='matches', viewset=MatchViewSet, base_name="match")
urlpatterns = router.urls