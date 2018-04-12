import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from sqlalchemy.exc import DBAPIError

from connectors.models import Connector
from connectors.utils import create_engine
from .utils import SourceParser
from .models import Table
from .serializers import PreviewSerializer


class PreviewAPIView(APIView):

    def get(self, request):
        file_name = request.GET.get('file_name')
        sep = request.GET.get('sep', ',')
        encoding = request.GET.get('encoding', 'utf-8')

        columns, content, dtype, count = SourceParser.read_csv(file_name,
                                                               sep=sep,
                                                               encoding=encoding)
        schema = json.dumps(dict(zip(columns, dtype)))
        serializer = PreviewSerializer(Table(columns=json.dumps(columns),
                                             sample=json.dumps(content),
                                             schema=json.dumps(schema)))
        return Response(serializer.data)


class QueryAPIView(APIView):
    def get(self, request):
        connector = Connector.objects.get(conn_name=request.GET.get('conn_name'))
        sql = request.GET.get('sql')
        try:
            engine = create_engine(db_type=connector.db_type,
                                   host=connector.host,
                                   port=connector.port,
                                   user=connector.user,
                                   password=connector.password,
                                   db_instance=connector.db_instance)
        except DBAPIError as err:
            print(err.args)
            Response(status=status.HTTP_400_BAD_REQUEST)

        columns, content, dtype, count = SourceParser.query_sql(sql, engine)
        schema = json.dumps(dict(zip(columns, dtype)))
        serializer = PreviewSerializer(Table(columns=json.dumps(columns),
                                             sample=json.dumps(content),
                                             schema=json.dumps(schema)))
        return Response(serializer.data)
