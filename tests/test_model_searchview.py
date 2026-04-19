from linkarchivetools.model import (
   DbConnection,
   SearchView,
)
from linkarchivetools.utils.reflected import (
   ReflectedEntryTable,
)

from .dbtestcase import DbTestCase


class SearchViewTest(DbTestCase):
    def test_constructor(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        controller = SearchView(connection=connection)
        controller.truncate()

        self.assertEqual(controller.count(), 0)

    def test_add(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        controller = SearchView(connection=connection)
        controller.truncate()

        self.assertEqual(controller.count(), 0)

        view_id = controller.add()
        self.assertTrue(view_id is not None)

    def test_get(self):
        self.create_db("input.db")
        self.clean_out()

        connection = DbConnection("input.db")

        controller = SearchView(connection=connection)
        controller.truncate()
        self.assertEqual(controller.count(), 0)

        view_id = controller.get()
        self.assertTrue(view_id is not None)
