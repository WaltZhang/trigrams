from django.db import models


class Connector(models.Model):
    MYSQL = 'mysql'
    POSTGRE = 'postgresql'
    ORACLE = 'oracle'
    DB_TYPES = [
        (MYSQL, 'mysql'),
        (POSTGRE, 'postgresql'),
        (ORACLE, 'oracle'),
    ]
    conn_name = models.CharField(max_length=20)
    db_type = models.CharField(max_length=10, choices=DB_TYPES)
    host = models.CharField(max_length=200)
    port = models.IntegerField()
    user = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=256, blank=True)
    db_instance = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.conn_name
