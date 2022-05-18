from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'bets', views.BetViewSet)
router.register(r'cats_hedgehogs', views.CatHedgehogViewSet)
router.register(r'lots', views.LotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bets/<int:pk>/accept', views.accept_bet, name='accept-bet')
]
