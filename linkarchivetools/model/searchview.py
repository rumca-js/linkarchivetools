from .basetable import BaseTable

class SearchView(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("searchview")

    def get(self, id=None):
        if id is not None:
            return super().get(id=id)

        views = self.get_where({})
        for view in views:
            return view

        view_id = self.add()

        return self.get(id=view_id)

    def add(self):
        json_data = {}
        json_data["name"] = "default"
        json_data["default"] = True
        json_data["priority"] = 0
        json_data["filter_statement"] = ""
        json_data["hover_text"] = ""
        json_data["icon"] = ""
        json_data["order_by"] = ""
        json_data["entry_limit"] = 0
        json_data["auto_fetch"] = False
        json_data["date_published_day_limit"] = 0
        json_data["date_created_day_limit"] = 0
        json_data["user"] = False

        return self.get_table().insert_json_data(json_data=json_data)
