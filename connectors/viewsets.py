from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Connector
from .serializers import ConnectorSerializer


class ConnectorAPIView(APIView):
    def get(self, request):
        connectors = Connector.objects.all()
        serializer = ConnectorSerializer(connectors, many=True)
        return Response(data=serializer.data)
