from sqlalchemy import and_, or_, not_, func, MetaData, Table, select

from .omnisearch import (
    SingleSymbolEvaluator,
    EquationEvaluator,
    OmniSearch,
)


class AlchemySymbolEvaluator(SingleSymbolEvaluator):
    """
    return 1 if true
    """

    def __init__(self, table, ignore_case=False):
        self.table = table
        self.ignore_case = ignore_case

    def evaluate_complex_symbol(self, symbol, condition_data):
        # TODO make todo check if symbol exists in table?

        if condition_data[1] == "==":
            if self.ignore_case:
                column = self.table.c[condition_data[0]]
                return func.lower(column) == condition_data[2].lower()
            else:
                return self.table.c[condition_data[0]] == condition_data[2]

        if condition_data[1] == "!=":
            if self.ignore_case:
                column = self.table.c[condition_data[0]]
                return func.lower(column) != condition_data[2].lower()
            else:
                return self.table.c[condition_data[0]] != condition_data[2]

        if condition_data[1] == ">":
            return self.table.c[condition_data[0]] > condition_data[2]

        if condition_data[1] == "<":
            return self.table.c[condition_data[0]] < condition_data[2]

        if condition_data[1] == ">=":
            return self.table.c[condition_data[0]] >= condition_data[2]

        if condition_data[1] == "<=":
            return self.table.c[condition_data[0]] <= condition_data[2]

        if condition_data[1] == "=":
            symbol = condition_data[2]
            symbol = symbol.replace("*", "%")

            if self.ignore_case:
                return self.table.c[condition_data[0]].ilike(symbol)
            else:
                return self.table.c[condition_data[0]].like(symbol)

        raise IOError("Unsupported operator")

    def evaluate_simple_symbol(self, symbol):
        """
        TODO we could check by default if entry link == symbol, or sth
        """
        if self.ignore_case:
            symbol = symbol.replace("*", "%")
            return or_(
                self.table.c["link"].ilike(symbol),
                self.table.c["title"].ilike(symbol),
                self.table.c["description"].ilike(symbol),
            )
        else:
            symbol = symbol.replace("*", "%")
            return or_(
                self.table.c["link"].like(symbol),
                self.table.c["title"].like(symbol),
                self.table.c["description"].like(symbol),
            )


class AlchemyEquationEvaluator(EquationEvaluator):
    def evaluate_function(self, operation_symbol, function, args0, args1):
        if function == "And":  # & sign
            return and_(args0, args1)
        elif function == "Or":  # | sign
            return or_(args0, args1)
        elif function == "Not":  # ~ sign
            return not_(args0)
        else:
            raise NotImplementedError("Not implemented function: {}".format(function))


class AlchemyRowHandler(object):
    def handle_row(self, row):
        pass


class AlchemySearch(object):
    def __init__(self, db, search_term, row_handler=None, args=None, connection=None):
        self.db = db
        self.connection = connection
        self.search_term = search_term
        self.alchemy_row_handler = row_handler

        self.args = args

        if self.args and self.args.table:
            self.table_name = self.args.table
        else:
            self.table_name = "linkdatamodel"

        self.order_by_column_names = ["id"]
        if self.args and self.args.order_by:
            self.order_by_column_names = [self.args.order_by]

        self.get_destination_table()

    def search(self):
        rows = self.get_filtered_objects()

        for row in rows:
            self.alchemy_row_handler.handle_row(row)
            yield row

    def get_destination_table(self):
        # no _ char
        self.tables = {}
        self.tables["tags"] = self.get_meta_table("entrycompactedtags")
        self.tables["social"] = self.get_meta_table("socialdata")
        self.tables["source"] = self.get_meta_table("sourcedatamodel")
        self.tables["linkdatamodel"] = self.get_meta_table("linkdatamodel")

    def get_meta_table(self, table_name):
        metadata = MetaData()
        return Table(table_name, metadata, autoload_with=self.db)

    def get_query_conditions(self):
        ignore_case = False
        if self.args and self.args.ignore_case:
            ignore_case = True

        symbol_evaluator = AlchemySymbolEvaluator(self.tables["linkdatamodel"], ignore_case)
        equation_evaluator = AlchemyEquationEvaluator(
            self.search_term, symbol_evaluator
        )

        search = OmniSearch(self.search_term, equation_evaluator=equation_evaluator)
        combined_query_conditions = search.get_combined_query()
        return combined_query_conditions

    def get_table_column_name(self, order_by_thing):
        split = order_by_thing.split("__")
        if len(split) > 1:
            return split[0], split[1]
        if len(split) == 1:
            return self.table_name, split[0]
        return self.table_name, None

    def get_order_by_column(self):
        table_name, column_name = self.get_table_column_name(self.order_by_column_names[0])

        order_by_column = getattr(self.tables[table_name].c, column_name, None)

        if order_by_column is None:
            raise AttributeError(f"Invalid order_by column: {self.order_by_column_names}")

        return order_by_column

    def get_order_by_clause(self):
        order_by_column = self.get_order_by_column()

        if self.args:
            # Determine sorting order
            order_by_clause = (
                order_by_column.asc()
                if self.args.asc
                else order_by_column.desc() if self.args.desc else order_by_column.asc()
            )
        else:
            order_by_clause = order_by_column.asc()

        return order_by_clause

    def get_filtered_objects(self):
        combined_query_conditions = self.get_query_conditions()
        order_by_clause = self.get_order_by_clause()

        rows = []

        # Use select() for SQLAlchemy Core
        if self.table_name == "linkdatamodel":
            tags_table = self.tables["tags"]
            social_data = self.tables["social"]
            sources = self.tables["source"]
            linktable = self.tables["linkdatamodel"]

            stmt = (
                select(linktable,
                       *[
                           col.label(f"tags_{col.name}")
                           for col in tags_table.c
                       ],
                       *[
                           col.label(f"social_{col.name}")
                           for col in social_data.c
                       ],
                       *[
                           col.label(f"source_{col.name}")
                           for col in sources.c
                       ]
                       )

                .outerjoin(tags_table, linktable.c.id == tags_table.c.entry_id)
                .outerjoin(social_data, linktable.c.id == social_data.c.entry_id)
                .outerjoin(sources, linktable.c.source_id == sources.c.id)

                .where(combined_query_conditions)
                .order_by(order_by_clause)
            )
        else:
            stmt = (
                select(linktable)
                .where(combined_query_conditions)
                .order_by(order_by_clause)
            )

        # Execute the query
        result = self.connection.execute(stmt)

        # Fetch all results
        rows = result.fetchall()

        return rows
