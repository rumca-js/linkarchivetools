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

    def count(self, table_name):
        row_count = self.connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar()
        return row_count

    def print_summary(self, print_columns=False):
        tables = self.get_table_names()

        for table in tables:
            row_count = self.connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar()
            print(f"Table: {table}, Row count: {row_count}")

            columns = self.get_column_names(table)
            if print_columns:
                column_names = [column["name"] for column in columns]
                print(f"Columns in {table}: {', '.join(column_names)}")


    def get_table_names(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return list(tables)

    def get_column_names(self, table):
        inspector = inspect(self.engine)
        row_count = self.connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar()

        columns = inspector.get_columns(table)
        column_names = [column["name"] for column in columns]
        return column_names

    def row_to_json_data(self, row):
        data = dict(row._mapping)
        return data

    def run_sql(self, sql_text):
        self.connection.execute(text(sql_text))
        self.connection.commit()


class ReflectedGenericTable(object):
    def __init__(self, engine, connection, table_name=None):
        self.engine = engine
        self.connection = connection
        self.table_name = table_name
        if self.table_name is None:
            self.table_name = self.get_table_name()

    def get_table_name():
        return self.table_name

    def get_table(self):
        destination_metadata = MetaData()
        destination_table = Table(
            self.table_name, destination_metadata, autoload_with=self.engine
        )
        return destination_table

    def truncate(self):
        sql_text = f"DELETE FROM {self.table_name};"
        self.connection.execute(text(sql_text))
        self.connection.commit()

    def create_index(self, column_name):
        index_name = f"idx_{self.table.name}_{column_name}"
        index = Index(index_name, getattr(table.c, column_name))

        index.create(bind=self.engine)

    def insert_json_data(self, json_data: dict):
        table = self.get_table()

        stmt = (
            insert(table)
            .values(**json_data)
            .returning(table.c.id)
        )

        result = self.connection.execute(stmt)
        inserted_id = result.scalar_one()
        self.connection.commit()

        return inserted_id

    def count(self):
        row_count = self.connection.execute(
            text(f"SELECT COUNT(*) FROM {self.table_name}")
        ).scalar()
        return row_count

    def print_summary(self, print_columns=False):
        row_count = self.connection.execute(
            text(f"SELECT COUNT(*) FROM {self.table_name}")
        ).scalar()
        print(f"Table: {self.table_name}, Row count: {row_count}")

        columns = self.get_column_names()
        if print_columns:
            column_names = [column["name"] for column in columns]
            print(f"Columns in {self.table_name}: {', '.join(column_names)}")

    def get_column_names(self):
        inspector = inspect(self.engine)
        row_count = self.connection.execute(
            text(f"SELECT COUNT(*) FROM {self.table_name}")
        ).scalar()

        columns = inspector.get_columns(self.table_name)
        column_names = [column["name"] for column in columns]
        return column_names

    def row_to_json_data(self, row):
        data = dict(row._mapping)
        return data

    def run_sql(self, sql_text):
        self.connection.execute(text(sql_text))
        self.connection.commit()


class ReflectedEntryTable(ReflectedGenericTable):
    def get_table_name(self):
        return "linkdatamodel"

    def insert_entry_json(self, entry_json):
        if "link" not in entry_json:
            return

        if "source_url" not in entry_json:
            entry_json["source_url"] = ""
        if "permanent" not in entry_json:
            entry_json["permanent"] = False
        if "bookmarked" not in entry_json:
            entry_json["bookmarked"] = False
        if "status_code" not in entry_json:
            entry_json["status_code"] = 0
        if "contents_type" not in entry_json:
            entry_json["contents_type"] = 0
        if "page_rating_contents" not in entry_json:
            entry_json["page_rating_contents"] = 0
        if "page_rating_visits" not in entry_json:
            entry_json["page_rating_visits"] = 0
        if "page_rating_votes" not in entry_json:
            entry_json["page_rating_votes"] = 0
        if "page_rating" not in entry_json:
            entry_json["page_rating"] = 0

        return self.insert_json_data(entry_json)

    def get_entries(self):
        destination_table = self.get_table()

        entries_select = select(destination_table)

        result = self.connection.execute(entries_select)
        entries = result.fetchall()

        for entry in entries:
            yield entry

    def get_entries_good(self):
        destination_table = self.get_table()

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
        destination_table = self.get_table()

        stmt = (
            select(1)
            .where(destination_table.c.link == link)
            .limit(1)
        )

        result = self.connection.execute(stmt).scalar()
        return result is not None

    def is_entry_id(self, entry_id):
        destination_table = self.get_table()

        stmt = (
            select(1)
            .where(destination_table.c.id == entry_id)
            .limit(1)
        )

        result = self.connection.execute(stmt).scalar()
        return result is not None


class ReflectedUserTags(ReflectedGenericTable):
    def get_table_name(self):
        return "usertags"

    def get_tags_string(self, entry_id):
        destination_table = self.get_table()

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
        destination_table = self.get_table()

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        tags = []

        result = self.connection.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            tags.append(row.tag)

        return tags


class ReflectedEntryCompactedTags(ReflectedGenericTable):
    def get_table_name(self):
        return "entrycompactedtags"

    def get_tags_string(self, entry_id):
        destination_table = self.get_table()

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
        destination_table = self.get_table()

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        tags = []

        result = self.connection.execute(stmt)
        rows = result.fetchall()
        for row in rows:
            tags.append(row.tag)

        return tags


class ReflectedSourceTable(ReflectedGenericTable):
    def get_table_name(self):
        return "sourcedatamodel"

    def get_source(self, source_id):
        destination_table = self.get_table()

        stmt = select(destination_table).where(destination_table.c.id == source_id)

        result = self.connection.execute(stmt)
        return result.first()


class ReflectedSocialData(ReflectedGenericTable):
    def get_table_name(self):
        return "socialdata"

    def get(self, entry_id):
        destination_table = self.get_table()

        stmt = select(destination_table).where(destination_table.c.entry_id == entry_id)

        result = self.connection.execute(stmt)
        return result.first()

    def get_json(self, entry_id):
        row = self.get(entry_id)
        if row is None:
            return None

        data = self.row_to_json_data(row)
        return data


class EntryCopier(object):
    def __init__(self, src_engine, src_connection, dst_engine, dst_connection):
        self.src_engine = src_engine
        self.src_connection = src_connection

        self.dst_engine = dst_engine
        self.dst_connection = dst_connection

    def copy_entry(self, entry):
        """
        """
        entry_table = ReflectedEntryTable(self.dst_engine, self.dst_connection)
        data = entry_table.row_to_json_data(entry)
        del data["id"]
        new_entry_id = entry_table.insert_entry_json(data)
        if new_entry_id is not None:
            self.copy_tags(entry, new_entry_id)
            self.copy_social_data(entry, new_entry_id)
        return new_entry_id

    def copy_tags(self, entry, new_entry_id):
        source_entry_compacted_tags = ReflectedEntryCompactedTags(self.src_engine, self.src_connection)
        tags = source_entry_compacted_tags.get_tags(entry.id)

        entry_tag_data = {}
        for tag in tags:
            entry_tag_data["tag"] = tag
            entry_tag_data["entry_id"] = new_entry_id
            destination_entry_compacted_tags = ReflectedEntryCompactedTags(self.dst_engine, self.dst_connection)
            destination_entry_compacted_tags.insert_json_data(entry_tag_data)

    def copy_social_data(self, entry, new_entry_id):
        source_entry_social_data = ReflectedSocialData(self.src_engine, self.src_connection)
        social_data = source_entry_social_data.get_json(entry.id)
        if social_data:
            if "id" in social_data:
                del social_data["id"]
            social_data["entry_id"] = new_entry_id

            destination_entry_social_data = ReflectedSocialData(self.dst_engine, self.dst_connection)
            destination_entry_social_data.insert_json_data(social_data)
