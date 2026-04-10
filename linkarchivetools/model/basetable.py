
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

    def truncate(self):
        self.get_table().truncate()

    def count(self):
        return self.get_table().count()
