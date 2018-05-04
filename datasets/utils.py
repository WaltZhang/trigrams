import os
import pandas as pd
from trigrams import settings


class SourceParser:
    @classmethod
    def read_excel(cls, io, sheet_name=0, header=0, skip_footer=0, names=None, dtype=None):
        df = pd.read_excel(io=io, sheet_name=sheet_name, header=header,
                        skip_footer=skip_footer, names=names, dtype=dtype,
                        na_values='', keep_default_na=False, engine='xlrd')
        count = df.shape[0]
        excel_dict = df[:200].to_dict('split')
        columns = excel_dict.get('columns')
        content = excel_dict.get('data')
        types = SourceParser.get_column_type(df)
        return columns, content, types, count

    @classmethod
    def get_excel_sheet_names(cls, io):
        xls = pd.ExcelFile(io=io)
        return xls.sheet_names

    @classmethod
    def read_csv(cls, file_name, sep=',', names=None, dtype=None, encoding=None):
        df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, file_name),
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
        df = pd.read_sql(sql=sql, con=con, columns=columns)
        count = df.shape[0]
        sql_dict = df[:200].to_dict('split')
        columns = sql_dict.get('columns')
        content = sql_dict.get('data')
        types = SourceParser.get_column_type(df)
        return columns, content, types, count
