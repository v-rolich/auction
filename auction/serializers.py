from rest_framework import serializers

from .models import Bet, CatHedgehog, Lot, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'balance']


class BetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Bet
        fields = ['url', 'id', 'lot', 'rate', 'owner']


class CatHedgehogSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = CatHedgehog
        fields = ['url', 'id', 'breed', 'name', 'owner']


class LotSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    bets = serializers.HyperlinkedIdentityField(many=True, view_name='bet-detail', format='html')

    class Meta:
        model = Lot
        fields = ['url', 'id', 'pet', 'price', 'owner', 'bets']
