from rest_framework import permissions, renderers, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db import transaction

from .models import Bet, CatHedgehog, Lot, User
from .permissions import IsOwnerOrReadOnly
from .serializers import BetSerializer, CatHedgehogSerializer, LotSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BetViewSet(viewsets.ModelViewSet):
    """
    Bet viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CatHedgehogViewSet(viewsets.ModelViewSet):
    """
    CatHedgehog viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = CatHedgehog.objects.all()
    serializer_class = CatHedgehogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LotViewSet(viewsets.ModelViewSet):
    """
    Lot viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['POST'])
def accept_bet(request, pk):
    try:
        bet = Bet.objects.get(pk=pk)
    except Bet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # import pdb; pdb.set_trace()
    return make_transaction(bet)


def make_transaction(bet):
    try:
        lot = bet.lot
        payer = bet.owner
        receiver = lot.owner
        amount = bet.rate
    except ObjectDoesNotExist or FieldDoesNotExist:
        return Response(
            data={"Error": "Object or field does not exist. Transaction failed"},
            status=status.HTTP_404_NOT_FOUND
        )

    if payer.balance < amount:
        return Response(data={"Fail": "Insufficient funds to pay"}, status=status.HTTP_403_FORBIDDEN)

    with transaction.atomic():
        payer.balance -= amount
        payer.save()
        receiver.balance += amount
        receiver.save()

        change_owner(bet)

        lot.delete()
        lot.save()

    return Response(data={"Success": "Deal has been completed successfully"}, status=status.HTTP_200_OK)


def change_owner(bet):
    pet = bet.lot.pet
    pet.owner = bet.owner
    pet.save()
