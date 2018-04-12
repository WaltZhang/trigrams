import os, json
from pandas import read_csv, read_sql
from trigrams import settings


class SourceParser:

    @classmethod
    def read_csv(cls, file_name, sep=',', names=None, dtype=None, encoding=None):
        df = read_csv(os.path.join(settings.MEDIA_ROOT, file_name),
                      sep=sep,
                      names=names,
                      dtype=dtype,
                      encoding=encoding,
                      na_filter=False)
        count = df.shape[0]
        csv_dict = df[:200].to_dict('split')
        columns = csv_dict.get('columns')
        content = csv_dict.get('data')
        types = SourceParser.get_column_type(df)
        return columns, content, types, count

    @classmethod
    def get_column_type(cls, df):
        dts = []
        for dt in df.dtypes.tolist():
            dts.append(str(dt))
        return dts

    @classmethod
    def query_sql(cls, sql, con, columns=None):
        df = read_sql(sql=sql, con=con, columns=columns)
        count = df.shape[0]
        sql_dict = df[:200].to_dict('split')
        columns = sql_dict.get('columns')
        content = sql_dict.get('data')
        types = SourceParser.get_column_type(df)
        return columns, content, types, count

