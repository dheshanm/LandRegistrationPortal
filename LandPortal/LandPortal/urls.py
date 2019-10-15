"""LandPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, serializers, viewsets
import time

from main.models import Transaction, Block, Chain

class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))
    def to_native(self, value):
        epoch = datetime.datetime(1970,1,1)
        return int((value - epoch).total_seconds())

# Serializers define the API representation.
class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    timestamp = serializers.DateTimeField(format="%s.%f")
    # timestamp = TimestampField("timestamp") 
    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "LandHolder_aadhaar",
            "Land_state",
            "Land_district",
            "Land_taluk",
            "Land_village",
            "Land_survey_number",
            "Land_subdivision_number",
            "timestamp"
        ]

class BlockSerializer(serializers.HyperlinkedModelSerializer):
    timestamp = serializers.DateTimeField(format="%s.%f")
    # timestamp = TimestampField("timestamp") 
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Block
        fields = [
            "index",
            "transactions",
            "timestamp",
            "previous_hash",
            "nonce",
            "hash"
        ]

class ChainSerializer(serializers.HyperlinkedModelSerializer):
    chain = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Chain
        fields = [
            "length",
            "chain",
            "peers"
        ]

# ViewSets define the view behavior.
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

class ChainViewSet(viewsets.ModelViewSet):
    queryset = Chain.objects.all()
    serializer_class = ChainSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'chain', ChainViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
]
