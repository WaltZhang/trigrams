import os, json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from sqlalchemy.exc import DBAPIError
from xlrd import XLRDError
from pandas.io.parsers import CParserError

from connectors.models import Connector
from connectors.utils import create_connection
from trigrams import settings
from .utils import SourceParser
from .models import Table
from .serializers import PreviewSerializer


class PreviewAPIView(APIView):

    def get(self, request):
        file_name = request.GET.get('file_name')
        extension = request.GET.get('extension', '.csv')
        if extension == '.csv':
            sep = request.GET.get('sep', ',')
            encoding = request.GET.get('encoding', 'utf-8')
            try:
                columns, content, dtype, count = SourceParser.read_csv(file_name,
                                                                       sep=sep,
                                                                       encoding=encoding)
            except CParserError as err:
                print(err.args)
                Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            sheet_name = request.GET.get('sheet_name', 0)
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, self.request.GET.get('file_name'))
                if os.path.exists(file_path):
                    columns, content, dtype, count = SourceParser.read_excel(io=file_path, sheet_name=sheet_name)
            except XLRDError as err:
                print(err.args)
                Response(status=status.HTTP_400_BAD_REQUEST)
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
            connection = create_connection(db_type=connector.db_type,
                                           host=connector.host,
                                           port=connector.port,
                                           user=connector.username,
                                           password=connector.password,
                                           db_instance=connector.db_instance)
        except DBAPIError as err:
            print(err.args)
            Response(status=status.HTTP_400_BAD_REQUEST)

        columns, content, dtype, count = SourceParser.query_sql(sql, connection)
        schema = json.dumps(dict(zip(columns, dtype)))
        serializer = PreviewSerializer(Table(columns=json.dumps(columns),
                                             sample=json.dumps(content),
                                             schema=json.dumps(schema)))
        return Response(serializer.data)
