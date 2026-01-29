from sqlalchemy import (
    MetaData,
    Table,
    select,
    delete,
    or_,
    and_,
    exists,
    text,
    inspect,
    insert,
    update,
    Index,
)


class ReflectedTable(object):
    def __init__(self, engine, connection):
        self.engine = engine

    def truncate_table(self, table_name):
        sql_text = f"DELETE FROM {table_name};"

        with self.engine.begin() as connection:
            connection.execute(text(sql_text))

    def create_index(self, table, column_name):
        index_name = f"idx_{table.name}_{column_name}"
        index = Index(index_name, getattr(table.c, column_name))

        index.create(bind=self.engine)

    def vacuum(self):
        with self.engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute(text("VACUUM"))

    def close(self):
        pass

    def count(self, table_name):
        sql_text = text(f"SELECT COUNT(*) FROM {table_name}")
        with self.engine.connect() as connection:
            row_count = connection.execute(sql_text).scalar_one()
        return row_count

    def print_summary(self, print_columns=False):
        tables = self.get_table_names()

        for table in tables:
            row_count = self.count(table)
            print(f"Table: {table}, Row count: {row_count}")

            if print_columns:
                column_names = self.get_column_names(table)
                print(f"Columns in {table}: {', '.join(column_names)}")

    def get_table_names(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return list(tables)

    def get_column_names(self, table):
        inspector = inspect(self.engine)

        columns = inspector.get_columns(table)
        column_names = [column["name"] for column in columns]
        return column_names

    def row_to_json_data(self, row):
        data = dict(row._mapping)
        return data

    def run_sql(self, sql_text):
        with self.engine.begin() as connection:
            connection.execute(text(sql_text))


class ReflectedGenericTable(object):
    def __init__(self, engine, connection, table_name=None):
        self.engine = engine
        self.table_name = table_name
        if self.table_name is None:
            self.table_name = self.get_table_name()
        self.table = None

    def get_table_name():
        return self.table_name

    def get_table(self):
        if self.table is None:
            destination_metadata = MetaData()
            self.table = Table(
                self.table_name, destination_metadata, autoload_with=self.engine
            )
            return self.table
        return self.table

    def truncate(self):
        sql_text = f"DELETE FROM {self.table_name};"
        with self.engine.begin() as connection:
            result = connection.execute(text(sql_text))

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

        with self.engine.begin() as connection:
            result = connection.execute(stmt)
            inserted_id = result.scalar_one()

        return inserted_id

    def update_json_data(self, id, json_data):
        table = self.get_table()

        stmt = (
            update(table)
            .where(table.c.id == id)
            .values(**json_data)
        )

        with self.engine.begin() as connection:
            connection.execute(stmt)

    def count(self):
        sql = text(f"SELECT COUNT(*) FROM {self.table_name}")
        with self.engine.connect() as connection:
            row_count = connection.execute(sql).scalar_one()
        return row_count

    def get(self, id):
        table = self.get_table()
        stmt = select(table).where(table.c.id == id)

        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            return result.first()

    def get_where(self,
                  conditions_map: dict=None,
                  conditions=None,
                  order_by=None,
                  limit:int|None=None,
                  offset:int=0):
        """
        @param conditions_map can be passed as {"name": "Test"}
        @param conditions can be passed as [destionation_table.c.rating > 5]
        @param order_by can be passed as [destionation_table.c.name.asc()]
        """
        destination_table = self.get_table()

        if not conditions:
            conditions = []

        if not conditions and conditions_map:
            for column_name, value in conditions_map.items():
                if not hasattr(destination_table.c, column_name):
                    raise ValueError(f"Unknown column: {column_name}")

                conditions.append(getattr(destination_table.c, column_name) == value)

        stmt = select(destination_table)

        if conditions:
            stmt = stmt.where(or_(*conditions))
        if order_by:
            stmt = stmt.order_by(*order_by)
        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            rows = result.fetchall()  # fetch all rows immediately

        return rows

    def delete(self, id):
        table = self.get_table()
        stmt = delete(table).where(table.c.id == id)

        with self.engine.begin() as connection:
            result = connection.execute(stmt)
            rowcount = result.rowcount  # number of rows deleted

        return rowcount

    def delete_where(self, conditions: dict):
        table = self.get_table()

        filters = []
        for column_name, value in conditions.items():
            if not hasattr(table.c, column_name):
                raise ValueError(f"Unknown column: {column_name}")
            filters.append(getattr(table.c, column_name) == value)

        stmt = delete(table).where(and_(*filters))

        with self.engine.begin() as connection:
            result = connection.execute(stmt)
            rowcount = result.rowcount  # number of rows deleted

        return rowcount

    def print_summary(self, print_columns=False):
        row_count = self.count()
        print(f"Table: {self.table_name}, Row count: {row_count}")

        if print_columns:
            column_names = self.get_column_names()
            print(f"Columns in {self.table_name}: {', '.join(column_names)}")

    def get_column_names(self):
        inspector = inspect(self.engine)

        with self.engine.connect() as connection:
            row_count = connection.execute(text(f"SELECT COUNT(*) FROM {self.table_name}")).scalar_one()

        columns = inspector.get_columns(self.table_name)
        column_names = [column["name"] for column in columns]
        return column_names

    def row_to_json_data(self, row):
        """
        Convert SQLAlchemy row to a dict
        """
        return dict(row._mapping)

    def run_sql(self, sql_text):
        with self.engine.begin() as connection:
            connection.execute(text(sql_text))


class ReflectedEntryTable(ReflectedGenericTable):
    def get_table_name(self):
        return "linkdatamodel"

    def insert_json(self, entry_json):
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

    def get_entries(self, limit: int | None = None, offset: int = 0):
        """
        TODO remove use get_where
        """
        table = self.get_table()
        stmt = select(table)

        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            rows = result.fetchall()  # fetch all rows immediately
        return rows

    def get_entries_good(self):
        """
        TODO remove use get_where
        """
        table = self.get_table()
        stmt = (
            select(table)
            .where(table.c.page_rating_votes > 0)
            .order_by(table.c.page_rating_votes.desc())
        )

        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            rows = result.fetchall()  # fetch all rows immediately
        return rows

    def exists(self, *, id=None, link=None):
        table = self.get_table()

        conditions = []
        if id is not None:
            conditions.append(table.c.id == id)
        if link is not None:
            conditions.append(table.c.link == link)

        if not conditions:
            return False

        stmt = select(exists().where(or_(*conditions)))

        with self.engine.connect() as connection:
            return connection.execute(stmt).scalar()


class ReflectedUserTags(ReflectedGenericTable):
    def get_table_name(self):
        return "usertags"

    def get_tags_string(self, entry_id):
        table = self.get_table()
        stmt = select(table).where(table.c.entry_id == entry_id)

        tags_list = []

        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            for row in result:
                tags_list.append(f"#{row.tag}")

        return ", ".join(tags_list)

    def get_tags(self, entry_id):
        table = self.get_table()
        stmt = select(table).where(table.c.entry_id == entry_id)

        tags = []
        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            for row in result:
                tags.append(row.tag)

        return tags


class ReflectedEntryCompactedTags(ReflectedGenericTable):
    def get_table_name(self):
        return "entrycompactedtags"

    def get_tags(self, entry_id):
        """Return a list of tag strings for the given entry_id."""
        table = self.get_table()
        stmt = select(table).where(table.c.entry_id == entry_id)

        tags = []
        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            for row in result:
                tags.append(row.tag)

        return tags


    def get_tags_string(self, entry_id):
        """Return tags for the given entry_id as a single string formatted as '#tag1, #tag2'."""
        table = self.get_table()
        stmt = select(table).where(table.c.entry_id == entry_id)

        tags_list = []
        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            for row in result:
                tags_list.append(f"#{row.tag}")

        return ", ".join(tags_list)


class ReflectedSourceTable(ReflectedGenericTable):
    def get_table_name(self):
        return "sourcedatamodel"

    def get_source(self, source_id):
        """Return a single source row by ID, or None if not found."""
        table = self.get_table()
        stmt = select(table).where(table.c.id == source_id)

        with self.engine.connect() as connection:
            return connection.execute(stmt).first()

    def get_sources(self, limit: int | None = None, offset: int = 0):
        """Yield sources with optional offset and limit."""
        table = self.get_table()
        stmt = select(table)

        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        with self.engine.connect() as connection:
            result = connection.execute(stmt)
            sources = result.fetchall()
        return sources

    def insert_json(self, source_json: dict):
        """Insert a source JSON dict, ensuring 'url' key exists."""
        source_json.setdefault("url", "")
        return self.insert_json_data(source_json)

    def exists(self, *, id=None, url=None):
        """Return True if a source with given ID or URL exists."""
        table = self.get_table()

        conditions = []
        if id is not None:
            conditions.append(table.c.id == id)
        if url is not None:
            conditions.append(table.c.url == url)

        if not conditions:
            return False

        stmt = select(exists().where(or_(*conditions)))

        with self.engine.connect() as connection:
            return connection.execute(stmt).scalar()


class ReflectedSocialData(ReflectedGenericTable):
    def get_table_name(self):
        return "socialdata"

    def get(self, entry_id):
        """Return a single row matching entry_id, or None if not found."""
        table = self.get_table()
        stmt = select(table).where(table.c.entry_id == entry_id)

        with self.engine.connect() as connection:
            return connection.execute(stmt).first()


    def get_json(self, entry_id):
        """Return the row as a dict (JSON-style), or None if not found."""
        row = self.get(entry_id)
        if row is None:
            return None
        return self.row_to_json_data(row)


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
        new_entry_id = entry_table.insert_json(data)
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
