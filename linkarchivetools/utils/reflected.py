from sqlalchemy import MetaData, Table, select, text, inspect, insert
from sqlalchemy import Index


class ReflectedTable(object):
    def __init__(self, engine, connection):
        self.engine = engine
        self.connection = connection

    def get_table(self, table_name):
        destination_metadata = MetaData()
        destination_table = Table(
            table_name, destination_metadata, autoload_with=self.engine
        )
        return destination_table

    def truncate_table(self, table_name):
        sql_text = f"DELETE FROM {table_name};"
        self.connection.execute(text(sql_text))
        self.connection.commit()

    def create_index(self, table, column_name):
        index_name = f"idx_{table.name}_{column_name}"
        index = Index(index_name, getattr(table.c, column_name))

        index.create(bind=self.engine)

    def vacuum(self):
        self.connection.execute(text("VACUUM"))

    def close(self):
        pass

    def insert_json_data(self, table_name, json_data: dict):
        table = self.get_table(table_name)

        stmt = (
            insert(table)
            .values(**json_data)
            .returning(table.c.id)
        )

        result = self.connection.execute(stmt)
        inserted_id = result.scalar_one()
        self.connection.commit()

        return inserted_id

    def print_summary(self, print_columns=False):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()

        for table in tables:
            row_count = self.connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar()
            print(f"Table: {table}, Row count: {row_count}")

            if print_columns:
                columns = inspector.get_columns(table)
                column_names = [column["name"] for column in columns]
                print(f"Columns in {table}: {', '.join(column_names)}")

    def row_to_json_data(self, row):
        data = dict(row._mapping)
        return data

    def run_sql(self, sql_text):
        self.connection.execute(text(sql_text))
        self.connection.commit()


class ReflectedEntryTable(ReflectedTable):
    def truncate(self):
        self.truncate_table("linkdatamodel")

    def get_entries(self):
        destination_table = self.get_table("linkdatamodel")

        entries_select = select(destination_table)

        result = self.connection.execute(entries_select)
        entries = result.fetchall()

        for entry in entries:
            yield entry

    def get_entries_good(self):
        destination_table = self.get_table("linkdatamodel")

        stmt = (
            select(destination_table)
            .where(destination_table.c.page_rating_votes > 0)
            .order_by(destination_table.c.page_rating_votes.desc())
        )

        result = self.connection.execute(stmt)
        entries = result.fetchall()

        for entry in entries:
            yield entry

    def is_entry_link(self, link):
        destination_table = self.get_table("linkdatamodel")

        stmt = (
            select(1)
            .where(destination_table.c.link == link)
            .limit(1)
        )

        result = self.connection.execute(stmt).scalar()
        return result is not None


class ReflectedUserTags(ReflectedTable):
    def get_tags_string(self, entry_id):
        destination_table = self.get_table("usertags")

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        tags = ""

        result = self.connection.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            if tags:
                tags += ", "

            tags += "#" + row.tag

        return tags

    def get_tags(self, entry_id):
        destination_table = self.get_table("usertags")

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        tags = []

        result = self.connection.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            tags.append(row.tag)

        return tags


class ReflectedEntryCompactedTags(ReflectedTable):
    def get_tags_string(self, entry_id):
        destination_table = self.get_table("entrycompactedtags")

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        tags = ""

        result = self.connection.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            if tags:
                tags += ", "

            tags += "#" + row.tag

        return tags

    def get_tags(self, entry_id):
        destination_table = self.get_table("entrycompactedtags")

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        tags = []

        result = self.connection.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            tags.append(row.tag)

        return tags


class ReflectedSourceTable(ReflectedTable):
    def truncate(self):
        self.truncate_table("sourcedatamodel")

    def get_source(self, source_id):
        destination_table = self.get_table("sourcedatamodel")

        stmt = select(destination_table).where(destination_table.c.id == source_id)

        result = self.connection.execute(stmt)
        return result.first()


class ReflectedSocialData(ReflectedTable):
    def truncate(self):
        self.truncate_table("socialdata")

    def get(self, entry_id):
        destination_table = self.get_table("socialdata")

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        result = self.connection.execute(stmt)
        return result.first()

    def get_json(self, entry_id):
        row = self.get(entry_id)
        if row is None:
            return None

        data = self.row_to_json_data(row)
        return data
