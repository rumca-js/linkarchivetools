from sqlalchemy import MetaData, Table
from linkarchivetools.utils.reflected import (
    ReflectedGenericTable,
)

class BaseTable(object):
    def __init__(self, connection):
        self.connection = connection
        self.table_name = None

    def set_table(self, table_name):
        """
        Name from dbconnection
        """
        self.table_name = table_name

    def get_table(self):
        return getattr(self.connection, self.table_name)

    def get_meta_table(self, table_name):
        engine = self.connection.engine
        metadata = MetaData()
        return Table(table_name, metadata, autoload_with=engine)

    def get_reflected_table(self, table_name):
        engine = self.connection.engine
        connection = self.connection.connection

        return ReflectedGenericTable(engine=engine, connection=connection, table_name=table_name)

    def truncate(self):
        self.get_table().truncate()

    def count(self):
        return self.get_table().count()

    def get(self, id):
        return self.get_table().get(id=id)

    def insert_json_data(self, json_data):
        return self.get_table().insert_json_data(json_data=json_data)

    def get_where(self,
                  conditions_map: dict=None,
                  conditions=None,
                  order_by=None,
                  limit:int|None=None,
                  offset:int=0):
        return self.get_table().get_where(conditions_map=conditions_map,
                                          conditions=conditions,
                                          order_by=order_by,
                                          limit=limit,
                                          offset=offset)
